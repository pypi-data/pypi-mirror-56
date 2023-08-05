from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Boolean, Integer, Text
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import object_session
import datetime

Base = declarative_base()

class Section(Base):
    __tablename__ = 'section'
    __table_args__ = (
        UniqueConstraint('parent_id', 'number'),
        CheckConstraint('(parent_id IS NULL AND id = 0) OR (parent_id IS NOT NULL AND id <> 0)'),
        CheckConstraint('parent_id <> id')
    )
    
    __export_headers__ = ['number', 'name', 'abbreviation',]
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, CheckConstraint('number >= 0'), nullable=False, index=True)
    name = Column(String, index=True, nullable=False)
    abbreviation = Column(String, default='', nullable=False)
    parent_id = Column(Integer, ForeignKey('section.id'))
    
    parent = relationship("Section", remote_side=[id])
    subsections = relationship("Section", cascade='all, delete-orphan')
    books = relationship('Book', back_populates="section")
    
    @property
    def unpadded_full_number(self):
        number = []
        section = self
        while section.parent is not None:
            number.append(str(section.number))
            section = section.parent
        return '-'.join(reversed(number))
    
    @property
    def full_number(self):
        cls = type(self)
        digits = len(str(object_session(self).query(cls).order_by(
            cls.number.desc()).first().number))
        template = '{:0{digits}}'
        number = []
        section = self
        while section.parent is not None:
            number.append(template.format(section.number, digits=digits))
            section = section.parent
        return '-'.join(reversed(number))
    
    @property
    def full_abbreviation(self):
        abbr = []
        section = self
        while section.parent is not None:
            abbr.append(str(section.abbreviation))
            section = section.parent
        return '-'.join(reversed(abbr))
    
    def __repr__(self):
        return "<Section {0.unpadded_full_number} {0.name} {0.abbreviation}>".format(self)
    
    def __iter__(self):
        return [self.unpadded_full_number, self.name, self.abbreviation].__iter__()
    
    @classmethod
    def from_values(cls, session, full_number, name, abbr, *args):
        numbers = full_number.split('-')
        parent = session.query(cls).get(0)
        for c in numbers[0:-1]:
            parent = session.query(cls).filter(cls.number == c,
                cls.parent == parent).one()
        
        return cls(number=numbers[-1], name=name, abbreviation=abbr,
            parent=parent)

book_author = Table('book_author', Base.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('book_id', Integer, ForeignKey('book.id', ondelete='cascade'), nullable=False),
    Column('author_id', Integer, ForeignKey('author.id', ondelete='cascade'), nullable=False),
    UniqueConstraint('book_id', 'author_id')
)

class BookAuthor(Base):
    __table__ = book_author
    __mapper_args__ = {
            'confirm_deleted_rows': False
        }
    id = book_author.c.id
    book_id = book_author.c.book_id
    author_id = book_author.c.author_id
    
    book = relationship("Book")
    author = relationship("Author")

class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
            UniqueConstraint('text', 'book_id'),
        )
    
    __export_headers__ = ['text',]
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True, nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    
    book = relationship("Book", back_populates="tags")
    
    def __str__(self):
        return self.text
    
    def __iter__(self):
        return [self.text].__iter__()
    
    @classmethod
    def from_values(cls, session, text, *args):
        return cls(text=text)

class Author(Base):
    __tablename__ = 'author'
    
    __export_headers__ = ['name', 'about',]
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint("name <> ''"), unique=True, index=True, nullable=False)
    about = Column(Text, nullable=False, default='')
    
    books = relationship("Book", secondary=book_author, back_populates="authors")
    
    def __str__(self):
        return self.name
    
    def __iter__(self):
        return [self.name, self.about].__iter__()
    
    @classmethod
    def from_values(cls, session, name, about='', *args):
        return cls(name=name, about=about)

class Publisher(Base):
    __tablename__ = 'publisher'
    
    __export_headers__ = ['name', 'about',]
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint("name <> ''"), unique=True, index=True, nullable=False)
    about = Column(Text, nullable=False, default='')
    
    books = relationship("Book", back_populates="publisher")
    
    def __str__(self):
        return self.name
    
    def __iter__(self):
        return [self.name, self.about].__iter__()
    
    @classmethod
    def from_values(cls, session, name, about='', *args):
        return cls(name=name, about=about)

class Library(Base):
    __tablename__ = 'library'
    
    __export_headers__ = ['name',]
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint("name <> ''"), unique=True, index=True, nullable=False)
    
    books = relationship("Book", back_populates="library")
    
    def __str__(self):
        return self.name
    
    def __iter__(self):
        return [self.name].__iter__()
    
    @classmethod
    def from_values(cls, session, name, *args):
        return cls(name=name)

class Book(Base):
    __tablename__ = 'book'
    
    __export_headers__ = [
        'number', 'title', 'authors', 'publisher', 'publication year',
        'library', 'is electronic?', 'language', 'tags',
    ]
    
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(
            Integer,
            ForeignKey('section.id'),
            CheckConstraint('section_id <> 0'),
            nullable=False
        )
    number = Column(
            Integer,
            CheckConstraint('number > 0'),
            nullable=False,
            index=True
        )
    title = Column(
            String,
            CheckConstraint("title <> ''"),
            index=True,
            nullable=False
        )
    publication_year = Column(
            Integer,
            CheckConstraint('number > 0'),
            index=True
        )
    
    publisher_id = Column(Integer, ForeignKey('publisher.id'))
    library_id = Column(Integer, ForeignKey('library.id'))
    is_electronic = Column(Boolean,  nullable=False, index=True)
    language = Column(String, index=True, nullable=False)
    
    section = relationship("Section", back_populates="books")
    authors = relationship("Author", secondary=book_author, back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    library = relationship("Library", back_populates="books")
    borrows = relationship("Borrow", cascade='all, delete-orphan')
    tags = relationship("Tag", back_populates="book",
        cascade='all, delete-orphan')
    
    @property
    def unpadded_full_number(self):
        return '{}-{}'.format(self.section.unpadded_full_number, self.number)
    
    @property
    def full_number(self):
        cls = type(self)
        digits = len(str(object_session(self).query(cls).order_by(
            cls.number.desc()).first().number))
        return '{}-{:0{digits}}'.format(self.section.full_number, self.number,
            digits=digits)
    
    @property
    def authors_names(self):
        return '|'.join([c.name for c in self.authors])
    
    @property
    def tags_text(self):
        return ' '.join([c.text for c in self.tags])
    
    @property
    def publisher_name(self):
        return self.publisher.name if self.publisher is not None else ''
    
    @property
    def publication_year_str(self):
        return self.publication_year if self.publication_year is not None else ''
    
    @property
    def library_name(self):
        return self.library.name if self.library is not None else ''
    
    @property
    def copies(self):
        session = object_session(self)
        q = session.query(type(self)).filter(
            section_id=self.section_id, number=self.number)
        return q.all()
    
    @property
    def copies_count(self):
        session = object_session(self)
        q = session.query(type(self)).filter(
            section_id=self.section_id, number=self.number)
        return q.count()
    
    def __repr__(self):
        return "<Book {0.unpadded_full_number} {0.title}>".format(self)
    
    def __iter__(self):
        if self.publisher is not None:
            publisher = self.publisher.name
        else:
            publisher = ''
        
        if self.library is not None:
            library = self.library.name
        else:
            library = ''
        
        return [self.unpadded_full_number, self.title, self.authors_names,
            publisher, self.publication_year, library, int(self.is_electronic),
            self.language, self.tags_text].__iter__()
    
    @classmethod
    def from_values(cls, session, full_number, title, authors_names='',
            publisher='', publication_year='', library='', is_electronic=False,
            language='', tags_text='', *args):
        numbers = full_number.split('-')
        section = session.query(Section).get(0)
        for c in numbers[0:-1]:
            section = session.query(Section).filter(Section.number == c,
                Section.parent == section).one()
        
        authors = [c.strip() for c in authors_names.split('|')]
        authors = [c for c in authors if c]
        for idx, c in enumerate(authors):
            try:
                authors[idx] = session.query(Author).filter(
                    Author.name == c).one()
            except NoResultFound:
                authors[idx] = Author(name=c)
        
        if publisher:
            try:
                publisher = session.query(Publisher).filter(
                    Publisher.name == publisher).one()
            except NoResultFound:
                publisher = Publisher(name=publisher)
        else:
            publisher = None
        
        if not publication_year:
            publication_year = None
        
        if library:
            try:
                library = session.query(Library).filter(
                    Library.name == library).one()
            except NoResultFound:
                library = Library(name=library)
        else:
            library = None
        
        tags = [c.strip() for c in tags_text.split()]
        tags = [Tag(text=c) for c in tags if c]
        
        return cls(number=numbers[-1], section=section, title=title,
            authors=authors, publisher=publisher,
            publication_year=publication_year, library=library,
            is_electronic=int(is_electronic), language=language, tags=tags)

class Borrow(Base):
    __tablename__ = 'borrow'
    
    __export_headers__ = [
        'book number', 'borrower', 'contact', 'date', 'return date',
    ]
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    borrower = Column(String, CheckConstraint("borrower <> ''"), index=True, nullable=False)
    contact = Column(String, CheckConstraint("contact not like '%[^0-9]%' AND contact <> ''"), index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False, default=datetime.datetime.now())
    return_date = Column(DateTime, index=True)
    
    book = relationship("Book", back_populates='borrows')
    
    @property
    def date_str(self):
        return '{:%Y-%m-%d}'.format(self.date)
    
    @property
    def return_date_str(self):
        if self.return_date is not None:
            return '{:%Y-%m-%d}'.format(self.return_date)
        else:
            return ''
    
    def return_(self):
        self.return_date = datetime.datetime.now()
    
    def __repr__(self):
        return "<Borrow {0.book.unpadded_full_number} {0.borrower} {0.date:%Y%m%d}>".format(self)
    
    def __iter__(self):
        if self.return_date is not None:
            return_date = '{:%Y-%m-%d}'.format(self.return_date)
        else:
            return_date = ''
        return [self.book.unpadded_full_number, self.borrower, self.contact,
            '{:%Y-%m-%d}'.format(self.date), return_date].__iter__()
    
    @classmethod
    def from_values(cls, session, full_number, borrower, contact, date,
            return_date, *args):
        numbers = full_number.split('-')
        section = session.query(Section).get(0)
        for c in numbers[0:-1]:
            section = session.query(Section).filter(Section.number == c,
                Section.parent == section).one()
        book = session.query(Book).filter(Book.number == numbers[-1],
                Book.section == section).one()
        
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        
        if return_date:
            return_date = datetime.datetime.strptime(return_date, '%Y-%m-%d')
        else:
            return_date = None
        
        return cls(book=book, borrower=borrower, contact=contact, date=date,
            return_date=return_date)

def default_args(args, defaults, headers=[]):
    args = list(args)
    for c in range(len(defaults)):
        if len(args) < c:
            if defaults[c] is None:
                raise ValueError('`{}` missing'.format(headers[c]))
            else:
                args.append(defaults[c])
        elif args[c] == '':
            if defaults[c] is None:
                raise ValueError('`{}` missing'.format(headers[c]))
            else:
                args[c] = defaults[c]
    
    return args

CLASSES = [
        Library,
        Author,
        Publisher,
        Section,
        Book,
        Borrow,
    ]
