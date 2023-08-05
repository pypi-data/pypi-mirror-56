from . import db
from .iqra_plugins import IqraCommand
from . import IqraCmd
from sqlalchemy import String
from sqlalchemy import func

class new(IqraCommand):
    'create a new section or book'
    
    class section(IqraCommand):
        'create a new section'
        
        args = (
            (['number'], dict(type=str, help='section number including all parent sections')),
            (['name'], dict(type=str, help='section name')),
            (['abbr'], dict(type=str, help='section abbreviation')),
        )
        
        def call(self, number, name, abbr):
            number = [int(c) for c in number.split('-')]
            
            session = self.util.get_scoped_session()
            
            section = self.util.get_root_section(session)
            for c in number[0:-1]:
                section = session.query(db.Section).filter(
                    db.Section.number == c, db.Section.parent == section).one()
            
            section = db.Section(number=number[-1],
                name=name, abbreviation=abbr, parent=section)
            
            session.add(section)
            return session
    
    class book(IqraCommand):
        'create a new book'
        
        args = (
            (['number'], dict(type=str, help='book number including all parent sections')),
            (['title'], dict(type=str, help='book title')),
            (['-p', '--publisher'], dict(type=str, help='publisher')),
            (['-a', '--authors'], dict(type=str, help='comma separated author names')),
            (['-l', '--library'], dict(type=str, help='library name')),
            (['-d', '--date'], dict(type=int, help='publication year')),
            (['-e', '--electronic'], dict(action='store_true', default=False, help='the book is an electronic book. opposite -ne')),
            (['-ne', '--not-electronic'], dict(action='store_false', dest='electronic', help='the book is a paper book. opposite -e')),
            (['--language'], dict(type=str, default='', help='language of the book')),
            (['--tags'], dict(type=str, default='', help='space seperated book tags')),
        )
        
        def call(self, number, title, publisher=None, authors=None,
                library=None, date=None, electronic=False, language='',
                tags=''):
            number = [int(c) for c in number.split('-')]
            
            session = self.util.get_scoped_session()
            section = self.util.get_root_section(session)
            for c in number[0:-1]:
                section = session.query(db.Section).filter(
                    db.Section.number == c, db.Section.parent == section).one()
            
            number = number[-1]
            
            if publisher is not None:
                obj = session.query(db.Publisher).filter(
                    db.Publisher.name == publisher).first()
                
                if obj is None:
                    obj = Publisher(name=publisher)
                
                publisher = obj
            
            if authors is not None:
                authors = [c.strip() for c in authors.split(',')]
                authors = [c for c in authors if c]
                for idx, c in enumerate(authors):
                    obj = session.query(db.Author).filter(
                        db.Author.name == c).first()
                    if obj is None:
                        obj = db.Author(name=c)
                    
                    authors[idx] = obj
            else:
                authors = []
            
            if library is not None:
                obj = session.query(db.Library).filter(
                    db.Library.name == library).first()
                
                if obj is None:
                    obj = Library(name=library)
                
                library = obj
            
            book = db.Book(number=number, section=section, title=title,
                publisher=publisher, authors=authors, library=library,
                publication_year=date, is_electronic=electronic,
                language=language
            )
            
            book_tags = [db.Tag(text=c, book=book) for c in tags.split()]
            
            session.add(book)
            session.add_all(book_tags)
    
    args = tuple()
    subcommands = [section, book]

class edit(IqraCommand):
    'edit a section or book'
    
    class section(IqraCommand):
        'edit a section'
        
        args = (
            (['old_number'], dict(type=str, help='current section number including all parent sections')),
            (['--number'], dict(type=str, default=None, help='new section number including all parent sections')),
            (['--name'], dict(type=str, default=None, help='new section name')),
            (['--abbr'], dict(type=str, default=None, help='new section abbreviation')),
        )
        
        def call(self, old_number, number, name, abbr):
            old_number = [int(c) for c in old_number.split('-')]
            
            session = self.util.get_scoped_session()
            section = self.util.get_root_section(session)
            for c in old_number:
                section = session.query(db.Section).filter(
                    db.Section.number == c, db.Section.parent == section).one()
            
            if number is not None:
                number = [int(c) for c in number.split('-')]
                new_parent = self.util.get_root_section(session)
                for c in number[0:-1]:
                    new_parent = session.query(db.Section).filter(
                        db.Section.number == c, db.Section.parent == new_parent).one()
                
                section.parent = new_parent
                section.number = number[-1]
            
            if name is not None:
                section.name = name
            
            if abbr is not None:
                section.abbr = abbr
    
    class book(IqraCommand):
        'edit a book'
        
        args = (
            (['old_number'], dict(type=str, help='old book number including all parent sections')),
            (['-n', '--number'], dict(type=str, default=None, help='new book number including all parent sections')),
            (['-t', '--title'], dict(type=str, default=None, help='new book title')),
            (['-p', '--publisher'], dict(type=str, default=None, help='new publisher')),
            (['-np', '--no-publisher'], dict(action='store_true', default=False, help='remove publisher')),
            (['-a', '--authors'], dict(type=str, default=None, help='new comma separated author names')),
            (['-l', '--library'], dict(type=str, default=None, help='new library name')),
            (['-nl', '--no-library'], dict(action='store_true', default=False, help='remove library')),
            (['-d', '--date'], dict(type=int, default=None, help='new publication year')),
            (['-nd', '--no-date'], dict(action='store_true', default=False, help='remove publication date')),
            (['-e', '--electronic'], dict(action='store_true', default=None, help='the book is an electronic book. opposite -ne')),
            (['-ne', '--not-electronic'], dict(action='store_false', dest='electronic', help='the book is a paper book. opposite -e')),
            (['--language'], dict(type=str, default=None, help='new language of the book')),
            (['--tags'], dict(type=str, default=None, help='new space seperated book tags')),
        )
        
        def call(self, old_number, number=None, title=None,
                publisher=None, no_publisher=False, authors=None, library=None,
                no_library=False, date=None, no_date=False, electronic=False,
                language=None, tags=None):
            old_number = [int(c) for c in old_number.split('-')]
            
            session = self.util.get_scoped_session()
            section = self.util.get_root_section(session)
            for c in old_number[0:-1]:
                section = session.query(db.Section).filter(
                    db.Section.number == c, db.Section.parent == section).one()
            
            old_number = old_number[-1]
            
            books = session.query(db.Book).filter_by(section=section,
                number=old_number).all()
            
            for book in books:
                if number is not None:
                    number = [int(c) for c in number.split('-')]
                
                    section = self.util.get_root_section(session)
                    for c in number[0:-1]:
                        section = session.query(db.Section).filter(
                            db.Section.number == c, db.Section.parent == section).one()
                    
                    book.section = section
                    book.number = number[-1]
                
                if title is not None:
                    book.title = title
                
                if no_publisher:
                    book.publisher = None
                elif publisher is not None:
                    obj = session.query(db.Publisher).filter(
                        db.Publisher.name == publisher).first()
                    
                    if obj is None:
                        obj = Publisher(name=publisher)
                    
                    book.publisher = obj
                
                if authors is not None:
                    authors = [c.strip() for c in authors.split(',')]
                    authors = [c for c in authors if c]
                    for idx, c in enumerate(authors):
                        obj = session.query(db.Author).filter(
                            db.Author.name == c).first()
                        if obj is None:
                            obj = db.Author(name=c)
                        
                        authors[idx] = obj
                    book.authors = authors
                
                if no_library:
                    book.library = None
                elif library is not None:
                    obj = session.query(db.Library).filter(
                        db.Library.name == library).first()
                    
                    if obj is None:
                        obj = db.Library(name=library)
                    
                    book.library = obj
                
                if no_date:
                    book.publication_year = None
                elif date is not None:
                    book.publication_year = date
                
                if electronic is not None:
                    book.is_electronic = electronic
                
                if language is not None:
                    book.language = language
                
                if tags is not None:
                    tags = [db.Tag(text=c, book=book) for c in tags.split()]
                    book.tags = tags
    
    args = tuple()
    subcommands = [section, book]

class delete(IqraCommand):
    'delete a book or section'
    
    class section(IqraCommand):
        'delete a section'
        
        args = (
            (['number'], dict(type=str, help='section number including all parent sections')),
        )
        
        def call(self, number):
            number = [int(c) for c in number.split('-')]
            
            session = self.util.get_scoped_session()
            section = self.util.get_root_section(session)
            for c in number:
                section = session.query(db.Section).filter(
                    db.Section.number == c, db.Section.parent == section).one()
            
            session.delete(section)
    
    class book(IqraCommand):
        'delete a book'
        
        args = (
            (['number'], dict(type=str, help='book number including all parent sections')),
            (['-i', '--index'], dict(type=int, default=0, help='book index (in case multiple copies of this book exists')),
        )
                
        def call(self, number, index):
            number = [int(c) for c in number.split('-')]
            
            session = self.util.get_scoped_session()
            section = self.util.get_root_section(session)
            for c in number[0:-1]:
                section = session.query(db.Section).filter(
                    db.Section.number == c, db.Section.parent == section).first()
            
            books = session.query(db.Book).filter(
                db.Book.section == section, db.Book.number == number[-1]
            ).offset(index).all()
            
            for book in books:
                session.delete(book)
    
    args = tuple()
    subcommands = [section, book]

class list_(IqraCommand):
    'list sections or books'
    name = 'list'
    
    class section(IqraCommand):
        'list sections'
        
        args = (
            (['number'], dict(type=int, default=0, nargs='?', help='max number of listed records')),
            (['-o', '--offset'], dict(type=int, default=0, help='list offset from first item')),
        )
                
        def call(self, number, offset):
            session = self.util.get_scoped_session()
            
            root_section = self.util.get_root_section(session)
            
            digits = self.util.get_section_digits()
            padding = digits * '0'
            full_number = func.substr(padding + db.Section.number.cast(String),
                -digits, digits)
            icteq = session.query(
                    db.Section.id,
                    full_number.label('number'),
                    db.Section.name,
                    db.Section.abbreviation,
                ).filter_by(
                    parent=root_section
                ).cte()
            rcteq = session.query(
                    db.Section.id,
                    icteq.c.number.concat('-').concat(full_number),
                    db.Section.name,
                    db.Section.abbreviation,
                ).join(
                    icteq, icteq.c.id == db.Section.parent_id
                )
            cteq = icteq.union(rcteq)
            
            q = session.query(cteq).order_by('number').offset(
                offset
            )
            if number > 0:
                q = q.limit(number)
            
            for pk, full_number, name, abbr in q:
                print(full_number, name, abbr)
    
    class book(IqraCommand):
        'list books'
        
        args = (
            (['number'], dict(type=int, default=10, nargs='?', help='max number of listed records')),
            (['-o', '--offset'], dict(type=int, default=0, help='list offset from first item')),
        )
                
        def call(self, number, offset):
            session = self.util.get_scoped_session()
            
            root_section = self.util.get_root_section(session)
            
            digits = self.util.get_section_digits()
            padding = digits * '0'
            full_number = func.substr(padding + db.Section.number.cast(String),
                -digits, digits)
            icteq = session.query(
                    db.Section.id,
                    full_number.label('number'),
                    db.Section.name,
                    db.Section.abbreviation
                ).filter_by(parent=root_section).cte()
            rcteq = session.query(
                    db.Section.id,
                    icteq.c.number.concat('-').concat(full_number),
                    db.Section.name,
                    db.Section.abbreviation
                ).join(
                    icteq, icteq.c.id == db.Section.parent_id
                )
            cteq = icteq.union(rcteq)
            
            subq = session.query(cteq).subquery()
            
            digits = self.util.get_book_digits()
            padding = digits * '0'
            book_number = func.substr(padding + db.Book.number.cast(String),
                -digits, digits)
            q = session.query(
                    db.Book,
                    func.count(db.Book.id),
                    subq.c.number.concat('-').concat(book_number)
                ).join(
                subq, subq.c.id == db.Book.section_id).order_by(
                subq.c.number, book_number).group_by(
                    db.Book.number, db.Book.section_id
                ).offset(offset).limit(number)
            
            for c, copies, number in q:
                if c.library is not None:
                    print(c.library.name)
                print(number, c.title, '({} copies)'.format(copies), c.language)
                print('tags:', *c.tags)
                print('authors:', *c.authors, sep=', ')
                
                publishing_info = []
                if c.publisher is not None:
                    publishing_info.append(c.publisher.name)
                if c.publication_year is not None:
                    publishing_info.append(str(c.publication_year))
                if publishing_info:
                    print(' '.join(publishing_info))
                if c.is_electronic:
                    print('electronic')
                else:
                    print('paper')
                
                print()
    
    args = tuple()
    subcommands = [section, book]

class file(IqraCommand):
    'execute commands from file'
    
    args = (
        (['name'], dict(type=str, help='file name to execute')),
    )
    
    def call(self, name):
        cmd = IqraCmd(util=self.util)
        
        with open(name, encoding='utf-8') as f:
            for c in f:
                cmd.onecmd(c)

class commit(IqraCommand):
    'commit database changes'
    
    args = tuple()
        
    def call(self):
        self.util.get_scoped_session().commit()

class rollback(IqraCommand):
    'rollback database changes'
    
    args = tuple()
        
    def call(self):
        self.util.get_scoped_session().rollback()

class echo(IqraCommand):
    'print message'
    
    args = (
        (['msg'], dict(type=str, nargs='*', help='message to print')),
    )
        
    @staticmethod
    def call(msg):
        print(*msg)

class backup(IqraCommand):
    'backup database'
    
    args = tuple()
        
    def call(self):
        self.util.backup()

class lsbackup(IqraCommand):
    'list existing database backups'
    
    args = tuple()
        
    def call(self):
        for c in self.util.list_backups():
            print(c.stem)

class restore(IqraCommand):
    'restore from backup'
    
    args = (
            (['dt'], dict(type=str, nargs='?', default=None, help='name of the backup file without extension as listed by `lsbackup` command. e.g. 20190807_112500')),
        )
    
    def call(self, dt=None):
        self.util.restore(dt)

class thumb(IqraCommand):
    'creates thumbnails for books. the created thumbnails are svg files containing the name of the book in a rectangle. if a thumbnail is found for a book, it will be ignored and no thumbnail will be generated.'
    
    args = (
        (['number'], dict(type=str, action='append', help='number of the book to generate thumb for.')),
    )
    
    def call(self, number):
        session = self.util.get_scoped_session()
        books = []
        for n in number:
            n = n.split('-')
            books.extend(self.util.get_books(session, *n).all())
        
        self._finished = 0
        self._total = len(books)
        
        for c in books:
            print(list(self.util.glob_path(
                    'res/thumbs/{}.*'.format(c.id))))
            if not len(list(self.util.glob_path(
                    'res/thumbs/{}.*'.format(c.id)))):
                self.util.generate_thumb(c)

