from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Query
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import CheckConstraint, UniqueConstraint
import datetime
from .. import db

Base = declarative_base()

class Section(Base):
    __tablename__ = 'section'
    __gui_metadata__ = {
            'combo': {'columns': ('id', 'number', 'name'), 'cast': (String,), 'extra_fields': {'text':'{number:0<section_digits>}-{name}'}},
            'dialog': ('number', 'name', 'abbreviation')
        }
    __query_metadata__ = {
            'order': ('number',)
        }
    __export_headers__ = [
            'Number',
            'Name',
            'Abbreviation',
        ]
    __import_class__ = db.Section
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, CheckConstraint('number >= 0'), unique=True, nullable=False, index=True)
    name = Column(String, CheckConstraint("name <> ''"), index=True, nullable=False)
    abbreviation = Column(String, default='', nullable=False)
    
    subsections = relationship("Subsection", back_populates="section", cascade='all, delete-orphan')
    books = relationship('Book',
        secondary="join(Subsection, Book)",
        primaryjoin="Section.id == Subsection.section_id",
        secondaryjoin="Subsection.id == Book.subsection_id",
        viewonly=True,
    )
    
    def __repr__(self):
        return "<Section {0.number:02} {0.name}>".format(self)
    
    def exporter(self):
        return [self.number, self.name, self.abbreviation]
    
    @classmethod
    def importer(class_, *args):
        args = default_args(args, [None, None, ''], class_.__export_headers__)
        return {'number': int(args[0]), 'name': args[1], 'abbreviation': args[2]}
    
    @classmethod
    def validator(class_, session, values):
        q = session.query(class_).filter(class_.number == values['number'])
        if q.count() > 0:
            raise ValueError('Section exists')
    
    def importdb(self, session):
        root_section = session.query(db.Section).get(0)
        return [db.Section(number=self.number, name=self.name,
            abbreviation=self.abbreviation, parent=root_section)]

class Subsection(Base):
    __tablename__ = 'subsection'
    __table_args__ = (UniqueConstraint('section_id', 'number'),)
    __gui_metadata__ = {
            'combo': {'columns': ('id', 'number', 'name', 'section_id'), 'cast': (String,), 'extra_fields': {'text':'{number:0<subsection_digits>}-{name}'}, 'chain': 'section'},
            'dialog': ('section', 'number', 'name', 'abbreviation')
        }
    __query_metadata__ = {
            'order': ('number',)
        }
    
    __export_headers__ = [
            'Number',
            'Name',
            'Abbreviation',
        ]
    __import_class__ = db.Section
    
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey('section.id'), nullable=False)
    number = Column(Integer, CheckConstraint('number >= 0'), nullable=False, index=True)
    name = Column(String, CheckConstraint("name <> ''"), index=True, nullable=False)
    abbreviation = Column(String, default='', nullable=False)
    
    section = relationship("Section", back_populates="subsections")
    books = relationship("Book", back_populates="subsection")
    
    def __repr__(self):
        return "<Subsection {0.section.number:02}-{0.number:02} {0.section.name}-{0.name}>".format(self)
    
    def exporter(self):
        number = '{0.section.number}-{0.number}'.format(self)
        return [number, self.name, self.abbreviation]
    
    @classmethod
    def importer(class_, *args):
        args = default_args(args, [None, None, ''], class_.__export_headers__)
        section_number, number = args[0].split('-')
        section = {'query': Query(Section).filter(
            Section.number == int(section_number))}
        return {'section': section,
            'number': int(number), 'name': args[1], 'abbreviation': args[2]}
    
    @classmethod
    def validator(class_, session, values):
        q = session.query(class_).filter(
            Subsection.section_id == values['section'].id,
            class_.number == values['number'])
        
        if q.count() > 0:
            raise ValueError('Subsection exists')
    
    def importdb(self, session):
        root_section = session.query(db.Section).get(0)
        parent = session.query(db.Section).filter(
            db.Section.parent == root_section,
            db.Section.number == self.section.number
        ).one()
        return [db.Section(number=self.number, name=self.name,
            abbreviation=self.abbreviation, parent=parent)]

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

class Author(Base):
    __tablename__ = 'author'
    __gui_metadata__ = {
            'combo': {'columns': ('id', 'name'), 'cast': (String,), 'labels': ('id',), 'text': 'name', 'with_entry': True},
            'dialog': ('name', 'about',)
        }
    __query_metadata__ = {
            'order': ('name',)
        }
    __export_headers__ = [
            'Name',
            'About',
        ]
    __import_class__ = db.Author
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint("name <> ''"), unique=True, index=True, nullable=False)
    about = Column(Text, nullable=False, default='')
    
    books = relationship("Book", secondary=book_author, back_populates="authors")
    
    def exporter(self):
        return [self.name, self.about]
    
    @classmethod
    def importer(class_, *args):
        args = default_args(args, [None, ''], class_.__export_headers__)
        return {'name': args[0], 'about': args[1]}
    
    @classmethod
    def validator(class_, session, values):
        q = session.query(class_).filter(class_.name == values['name'])
        if q.count() > 0:
            raise ValueError('Author exists')
    
    def importdb(self, session):
        return [db.Author(name=self.name, about=self.about)]

class Publisher(Base):
    __tablename__ = 'publisher'
    __gui_metadata__ = {
            'combo': {'columns': ('id', 'name'), 'cast': (String,), 'labels': ('id',), 'text': 'name', 'with_entry': True},
            'dialog': ('name', 'about',)
        }
    __query_metadata__ = {
            'order': ('name',)
        }
    __export_headers__ = [
            'Name',
            'About',
        ]
    __import_class__ = db.Publisher
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint("name <> ''"), unique=True, index=True, nullable=False)
    about = Column(Text, nullable=False, default='')
    
    books = relationship("Book", back_populates="publisher")
    
    def exporter(self):
        return [self.name, self.about]
    
    @classmethod
    def importer(class_, *args):
        args = default_args(args, [None, ''], class_.__export_headers__)
        return {'name': args[0], 'about': args[1]}
    
    @classmethod
    def validator(class_, session, values):
        q = session.query(class_).filter(class_.name == values['name'])
        if q.count() > 0:
            raise ValueError('Publisher exists')
    
    def importdb(self, session):
        return [db.Publisher(name=self.name, about=self.about)]

class Location(Base):
    __tablename__ = 'location'
    __gui_metadata__ = {
            'combo': {'columns': ('id', 'name'), 'cast': (String,), 'labels': ('id',), 'text': 'name'},
            'dialog': ('name',)
        }
    __query_metadata__ = {
            'order': ('name',)
        }
    __export_headers__ = [
            'Name',
        ]
    __import_class__ = db.Library
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint("name <> ''"), unique=True, index=True, nullable=False)
    
    books = relationship("Book", back_populates="location")
    
    def exporter(self):
        return [self.name]
    
    @classmethod
    def importer(class_, *args):
        args = default_args(args, [None], class_.__export_headers__)
        return {'name': args[0]}
    
    @classmethod
    def validator(class_, session, values):
        q = session.query(class_).filter(class_.name == values['name'])
        if q.count() > 0:
            raise ValueError('Location exists')
    
    def importdb(self, session):
        return [db.Library(name=self.name)]

class Book(Base):
    __tablename__ = 'book'
    __table_args__ = (UniqueConstraint('location_id', 'subsection_id', 'number'),)
    __gui_metadata__ = {
            'dialog': ('subsection', 'number', 'title', 'authors', 'publisher', 'location', 'copies'),
            'combo': {'columns': ('id', 'number', 'title', 'subsection_id'), 'cast': (String,), 'extra_fields': {'text':'{number:0<book_digits>}-{title}'}, 'chain': 'subsection'},
        }
    __many_relationships__ = {
            'authors': (BookAuthor, 'book_id', 'author_id')
        }
    __export_headers__ = [
            'Book Number',
            'Title',
            'Authors',
            'Publisher',
            'Location',
            'Copies',
        ]
    __import_class__ = db.Book
    
    id = Column(Integer, primary_key=True, index=True)
    section_id = association_proxy('subsection','section_id')
    subsection_id = Column(Integer, ForeignKey('subsection.id'), nullable=False)
    number = Column(Integer, CheckConstraint('number > 0'), nullable=False, index=True)
    title = Column(String, CheckConstraint("title <> ''"), index=True, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publisher.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    copies = Column(Integer, CheckConstraint('copies >= 0'), nullable=False, default=1)
    
    section = association_proxy('subsection','section')
    subsection = relationship("Subsection", back_populates="books")
    authors = relationship("Author", secondary=book_author, back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    location = relationship("Location", back_populates="books")
    borrows = relationship("Borrow", cascade='all, delete-orphan')
    
    def __repr__(self):
        return "<Book {0.section.number:02}-{0.subsection.number:02}-{0.number:04} {0.section.name}-{0.subsection.name}-{0.title}>".format(self)
    
    def exporter(self):
        book_number = '{}-{}-{}'.format(self.section.number, self.subsection.number, self.number)
        authors = ','.join([c.name for c in self.authors])
        if self.publisher is None:
            publisher = ''
        else:
            publisher = self.publisher.name
        if self.location is None:
            location = ''
        else:
            location = self.location.name
        return [
                book_number,
                self.title,
                authors,
                publisher,
                location,
                self.copies,
            ]
    
    @classmethod
    def importer(class_, *args):
        args = default_args(
            args, [None, None, '', '', '', 1], class_.__export_headers__)
        section_number, subsection_number, book_number = args[0].split('-')
        subsection = {'query': Query(Subsection).join(Section).filter(Section.number == int(section_number), Subsection.number == int(subsection_number))}
        if args[3]:
            publisher = {
                    'query': Query(Publisher).filter_by(name=args[3]),
                    'add': Publisher(name=args[3]),
                }
        else:
            publisher = None
        if args[4]:
            location = {
                    'query': Query(Location).filter_by(name=args[4]),
                    'add': Location(name=args[4])
                }
        else:
            location = None
        author_names = args[2].split(',')
        author_names = [name.strip() for name in author_names]
        author_names = [name for name in author_names if name]
        author_filters = [Author.name == name for name in author_names]
        author_adds = [Author(name=name) for name in author_names]
        return {
                'subsection': subsection,
                'number': int(book_number),
                'title': args[1],
                'publisher': publisher,
                'location': location,
                'copies': int(args[5]),
                BookAuthor: {
                        'rel_prop': 'authors',
                        'rel_query': Query(Author),
                        'filters': author_filters,
                        'adds': author_adds,
                    },
        }
    
    @classmethod
    def validator(class_, session, values):
        if values['location'] is not None:
            location_id = values['location'].id
        else:
            location_id = None
        q = session.query(class_).filter(
            class_.number == values['number'],
            class_.subsection_id == values['subsection'].id,
            class_.location_id == location_id)
        
        if values['number'] <= 0:
            raise ValueError('Invalid book number')
        elif values['copies'] < 0:
            raise ValueError('Invalid copies')
        elif q.count() > 0:
            raise ValueError('Book exists')
    
    def importdb(self, session):
        root_section = session.query(db.Section).get(0)
        section = session.query(db.Section).filter(
            db.Section.parent == root_section,
            db.Section.number == self.section.number
        ).one()
        subsection = session.query(db.Section).filter(
            db.Section.parent == section,
            db.Section.number == self.subsection.number
        ).one()
        if self.publisher is not None:
            publisher = session.query(db.Publisher).filter(
                db.Publisher.name == self.publisher.name).one()
        else:
            publisher = None
        author_names = [c.name for c in self.authors]
        if author_names:
            authors = session.query(db.Author).filter(
                db.Author.name.in_(author_names)).all()
        else:
            authors = []
        if self.location is not None:
            library = session.query(db.Library).filter(
                db.Library.name == self.location.name).one()
        else:
            library = None
        
        books = [db.Book(section=subsection, number=self.number,
            title=self.title, authors=authors, publisher=publisher,
            library=library, is_electronic=False, language=''
        ) for c in range(self.copies)]
        return books
            

class Borrow(Base):
    __tablename__ = 'borrow'
    __gui_metadata__ = {
            'dialog': ('book', 'borrower', 'contact'),
        }
    __export_headers__ = [
            'Book number',
            'Borrower',
            'Contact',
            'Date',
            'Return date',
        ]
    __import_class__ = db.Borrow
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    borrower = Column(String, CheckConstraint("borrower <> ''"), index=True, nullable=False)
    contact = Column(String, CheckConstraint("contact not like '%[^0-9]%' AND contact <> ''"), index=True, nullable=False)
    
    book = relationship("Book", back_populates='borrows')
    
    date = Column(DateTime, index=True, nullable=False, default=datetime.datetime.now())
    return_date = Column(DateTime, index=True)
    
    def return_(self):
        self.return_date = datetime.datetime.now()
    
    def exporter(self):
        book_number = '{}-{}-{}'.format(self.book.section.number, self.book.subsection.number, self.book.number)
        date = '{:%Y-%m-%d}'.format(self.date)
        if self.return_date is None:
            return_date = ''
        else:
            return_date = '{:%Y-%m-%d}'.format(self.return_date)
        
        return [
                book_number,
                self.borrower,
                self.contact,
                date,
                return_date
            ]
    
    @classmethod
    def importer(class_, *args):
        args = default_args(
            args, [None, None, None, None, ''], class_.__export_headers__)
        section_number, subsection_number, book_number = [int(c) for c in args[0].split('-')]
        book_id = {
                'query': Query(
                        Book
                    ).join(
                        Subsection
                    ).join(
                        Section, Section.id == Subsection.section_id
                    ).filter(
                        Section.number == section_number,
                        Subsection.number == subsection_number,
                        Book.number == book_number
                    )
            }
        
        date = datetime.datetime.strptime(args[3], '%Y-%m-%d')
        if args[4] != '':
            return_date = datetime.datetime.strptime(args[4], '%Y-%m-%d')
        else:
            return_date = None
        return {
                'book_id': book_id,
                'borrower': args[1],
                'contact': args[2],
                'date': date,
                'return_date': return_date,
            }
    
    def importdb(self, session):
        root_section = session.query(db.Section).get(0)
        section = session.query(db.Section).filter(parent=root_section,
            number=self.book.section.number).one()
        subsection = session.query(db.Section).filter(parent=section,
            number=self.book.subsection.number).one()
        book = session.query(db.Book).filter(section=subsection,
            number=self.book.number)
        
        return [db.Borrow(book=book, borrower=self.borrower,
            contact=self.contact, date=self.date, return_date=self.return_date)]

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

class Config(Base):
    __tablename__ = 'config'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, CheckConstraint("name <> ''"), index=True, nullable=False)
    value = Column(String)

CLASSES = (
        Location,
        Author,
        Publisher,
        Section,
        Subsection,
        Book,
        Borrow,
    )

