import sys
import csv
from .iqra_plugins import IqraPlugin
import importlib
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String
from sqlalchemy import func, text
from . import db
import argparse
try:
    import cairo
    import gi
    gi.require_version('Pango', '1.0')
    gi.require_version('PangoCairo', '1.0')
    
    from gi.repository import Pango
    from gi.repository import PangoCairo
except ImportError:
    cairo = None

class exportdb(IqraPlugin):
    'exports data to a csv file'
    
    args = (
        (['name'], dict(type=str, help='file name to export to')),
        (['-nl', '--no-library'], dict(action='append_const', const=db.Library, default=list(), dest='exclude', help='do not include libraries in the exported file')),
        (['-na', '--no-author'], dict(action='append_const', const=db.Author, dest='exclude', help='do not include authors in the exported file')),
        (['-np', '--no-publisher'], dict(action='append_const', const=db.Publisher, dest='exclude', help='do not include publishers in the exported file')),
        (['-ns', '--no-section'], dict(action='append_const', const=db.Section, dest='exclude', help='do not include sections in the exported file')),
        (['-nb', '--no-book'], dict(action='append_const', const=db.Book, dest='exclude', help='do not include books in the exported file')),
        (['--no-borrow'], dict(action='append_const', const=db.Borrow, dest='exclude', help='do not include borrows in the exported file')),
    )
    
    def do_call(self, name, exclude=tuple()):
        session = self.util.get_scoped_session()
        
        try:
            with open(name, 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                classes = {
                    c: session.query(c) for c in db.CLASSES if c not in exclude
                }
                if db.Section in classes:
                    classes[db.Section] = classes[db.Section].filter(
                        db.Section.parent_id != None)
                
                classes = {c: classes[c] for c in classes if classes[c].count()}
                self._finished = 0
                self._total = sum([classes[c].count() for c in classes])
                
                for c in classes:
                    try:
                        writer.writerow([''] + c.__export_headers__)
                    except AttributeError:
                        pass
                    
                    q = classes[c]
                    self._message = 'exporting {}'.format(c.__name__)
                    for d in q:
                        row = [type(d).__name__.casefold()]
                        row.extend(iter(d))
                        writer.writerow(row)
                        self.next()
                        if self._stop:
                            break
                    
                    if self._stop:
                        break
        except Exception as e:
            self._message = str(e)
            raise
        
        self._message = 'done'

class importdb(IqraPlugin):
    'imports data from an older version iqra database or from a csv file'
    
    args = (
        (['name'], dict(type=str, help='file name to import. if the extension is `db` or `-v` argument is given, will guess the file to be a database file. otherwise, will guess the file to be a csv file.')),
        (['-v', '--version'], dict(type=int, nargs='?', default=None, help='database version. if ommitted it will be guessed from file name (e.g. for `library_0.db`, version will be guessed as 0).')),
        (['-nl', '--no-library'], dict(action='append_const', const=db.Library, default=list(), dest='exclude', help='do not include libraries in the exported file')),
        (['-na', '--no-author'], dict(action='append_const', const=db.Author, dest='exclude', help='do not include authors in the exported file')),
        (['-np', '--no-publisher'], dict(action='append_const', const=db.Publisher, dest='exclude', help='do not include publishers in the exported file')),
        (['-ns', '--no-section'], dict(action='append_const', const=db.Section, dest='exclude', help='do not include sections in the exported file')),
        (['-nb', '--no-book'], dict(action='append_const', const=db.Book, dest='exclude', help='do not include books in the exported file')),
        (['--no-borrow'], dict(action='append_const', const=db.Borrow, dest='exclude', help='do not include borrows in the exported file')),
    )
    
    def do_call(self, name, version=None, exclude=[]):
        try:
            if version is not None or name.endswith('.db'):
                self.import_db(name, version, exclude)
            else:
                self.import_csv(name, exclude)
        except Exception as e:
            self._message = str(e)
            raise
    
    def import_csv(self, name, exclude=[]):
        tables = {c.__name__.casefold(): c for c in db.CLASSES if c not in exclude}
        session = self.util.get_scoped_session()
        with open(name, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            rows = tuple(reader)
            self._finished = 0
            self._total = len(rows)
            
            self._message = 'importing {}'.format(name)
            
            for c in rows:
                table = c[0].casefold()
                if table in tables:
                    session.add(tables[table].from_values(session, *c[1:]))
                self.next()
                if self._stop:
                    break
        
        self._message = 'done'
    
    def import_db(self, name, version=None, exclude=[]):
        if version is None:
            version = int(pathlib.Path(name).stem.split('_')[-1])
        
        uri = 'sqlite:///{}'.format(name)
        
        import_name = '{}.importers.db_{}'.format(__package__, version)
        
        old_db = importlib.import_module(import_name)
        
        engine = create_engine(uri)
        old_db.Base.metadata.create_all(engine)
        
        session = self.util.get_scoped_session()
        old_session = sessionmaker(bind=engine)()
        
        classes = [c for c in old_db.CLASSES if c.__import_class__ not in exclude]
        
        count = sum([old_session.query(cls).count() for cls in classes])
        self._finished = 0
        self._total = count
        try:
            for cls in classes:
                self._message = 'importing {}'.format(cls.__name__)
                for n, c in enumerate(old_session.query(cls)):
                    session.add_all(c.importdb(session))
                    self.next()
                    if self._stop:
                        break
                if self._stop:
                    session.rollback()
                    break
        finally:
            old_session.close()
        
        self._message = 'done'

class stickers(IqraPlugin):
    CONFIG = {
            'stickers_page_width': 210,
            'stickers_page_height': 297,
            'stickers_top_margin': 1.0,
            'stickers_left_margin': 1.0,
            'stickers_voffset': 0.0,
            'stickers_hoffset': 0.0,
            'stickers_columns': 4,
            'stickers_rows': 10,
            'stickers_row_sep': 1.0,
            'stickers_col_sep': 1.0,
            'stickers_border_width': 1.0,
            'stickers_border_color': [0, 0, 0],
            'stickers_font': 'Droid Arabic Kufi 10',
            'stickers_text_color': [0, 0, 0],
            'stickers_book_template': '{book.library.name}\n'
                                      '{book.full_number}\n'
                                      '{book.section.full_abbreviation}',
            'stickers_section_template': '{section.name}\n'
                                         '{section.full_number}',
            'stickers_library_template': '{library.name}',
        }
    
    args = (
        (['-f', '--file'], dict(type=str, default='-', help='file name in which to save stickers. giving `-` means stdout. defaults to `-`.')),
        (['-pdf'], dict(action='store_const', const=cairo.PDFSurface, default=None, dest='surface_cls', help='use pdf file format. by default, the format will be guessed from the file extension')),
        (['-ps'], dict(action='store_const', const=cairo.PSSurface, dest='surface_cls', help='use ps file format.')),
        (['items'], dict(nargs=argparse.REMAINDER, default='',
            help='items to generate stickers for. This can be one of '
                 '{section, book, library}'
            )),
    )
    
    SURFACE_EXT = {
        '.ps': cairo.PSSurface,
        '': cairo.PDFSurface
    }
    
    main_parser = argparse.ArgumentParser(prog='stickers')
    subparsers = main_parser.add_subparsers()
    
    parser = subparsers.add_parser('section')
    parser.set_defaults(cls=db.Section)
    parser.add_argument('-c', '--count', type=int, default=1)
    parser.add_argument('-r', '--range', nargs=2, action='append', default=[], dest='filters')
    parser.add_argument('-p', '--pattern', action='append', dest='filters')
    parser.add_argument('other_items', nargs=argparse.REMAINDER)
    
    parser = subparsers.add_parser('book')
    parser.set_defaults(cls=db.Book)
    parser.add_argument('-c', '--count', type=int, default=1)
    parser.add_argument('-r', '--range', nargs=2, action='append', default=[], dest='filters')
    parser.add_argument('-p', '--pattern', action='append', dest='filters')
    parser.add_argument('other_items', nargs=argparse.REMAINDER)
    
    parser = subparsers.add_parser('library')
    parser.set_defaults(cls=db.Library)
    parser.add_argument('-c', '--count', type=int, default=1)
    parser.add_argument('-p', '--pattern', action='append', default=[], dest='filters')
    parser.add_argument('other_items', nargs=argparse.REMAINDER)
    
    parser = subparsers.add_parser('blank')
    parser.set_defaults(cls=None)
    parser.set_defaults(filters=[])
    parser.add_argument('-c', '--count', type=int, default=1, dest='count')
    parser.add_argument('other_items', nargs=argparse.REMAINDER)
    
    def do_call(self, file=None, items=[], surface_cls=None, ctx=None,
            queries=None, config=None):
        if cairo is None:
            self._message = 'cairo library is missing. must install it.'
            raise RuntimeError(self.message)
        
        if file == '-':
            file = sys.stdout.buffer
        
        if config is None:
            config = {}
        for c in self.CONFIG:
            if c not in config:
                config[c] = type(self.CONFIG[c])(
                    self.util.get_config(c))
        
        cls_filters = {
            db.Section:
                {
                    list: lambda x: text('full_number BETWEEN :num_1 AND :num_2').bindparams(num_1=x[0], num_2=x[1]),
                    str: lambda x: text('section_name like :pattern').bindparams(pattern=x),
                },
            db.Book:
                {
                    list: lambda x: text('section_full_number || "-" || book.number BETWEEN :num_1 AND :num_2').bindparams(num_1=x[0], num_2=x[1]),
                    str: lambda x: db.Book.title.like(x),
                },
            db.Library:
                {
                    str: lambda x: db.Library.name.like(x),
                },
            }
        
        cls_queries = {
                db.Section: self.section_query(),
                db.Book: self.book_query(),
                db.Library: self.util.get_scoped_session().query(db.Library),
                None: self.util.get_scoped_session().query('NULL')
            }
        
        found_items = []
        while items:
            ns = vars(type(self).main_parser.parse_args(items))
            items = ns.pop('other_items')
            found_items.append(ns)
        
        if queries is None:
            queries = []
            for item in found_items:
                cls = item['cls']
                filters = item['filters']
                
                q = {}
                q['count'] = item['count']
                q['q'] = cls_queries[cls]
                if filters:
                    cond = filters.pop(0)
                    q['q'] = q['q'].filter(cls_filters[cls][type(cond)](cond))
                queries.append(q)
                
                for c in filters:
                    q = {}
                    q['count'] = item['count']
                    q['q'] = cls_queries[cls].filter(
                        cls_filters[cls][type(cond)](cond))
                    queries.append(q)
        
        self._finished = 0
        self._total = sum([c['count'] * c['q'].count() for c in queries])
        
        try:
            sur_finish = False
            if ctx is None:
                MM_IN_PT = 72 / 25.4
                ext = pathlib.Path(file).suffix
                if surface_cls is None:
                    if ext in type(self).SURFACE_EXT:
                        surface_cls = type(self).SURFACE_EXT[ext]
                    else:
                        surface_cls = type(self).SURFACE_EXT['']
                
                sur = surface_cls(file,
                    MM_IN_PT * self.util.get_config('stickers_page_width'),
                    MM_IN_PT * self.util.get_config('stickers_page_height'))
                ctx = cairo.Context(sur)
                sur_finish = True
            
            self.gen_stickers(ctx, *queries, config=config)
        except Exception as e:
            self._message = str(e)
            raise
        finally:
            if sur_finish:
                sur.finish()
        
    def gen_stickers(self, ctx, *queries, config=None):
        if config is None:
            config = {}
        for c in self.CONFIG:
            if c not in config:
                config[c] = type(self.CONFIG[c])(
                    self.util.get_config(c))
        
        MM_IN_PT = 72 / 25.4
        config['stickers_top_margin'] *= MM_IN_PT
        config['stickers_left_margin'] *= MM_IN_PT
        config['stickers_col_sep'] *= MM_IN_PT
        config['stickers_row_sep'] *= MM_IN_PT
        config['stickers_border_width'] *= MM_IN_PT
        config['stickers_page_width'] *= MM_IN_PT
        config['stickers_page_height'] *= MM_IN_PT
        
        w = (config['stickers_page_width'] - 2 * config['stickers_left_margin'] -
                (config['stickers_columns'] - 1) * 2 *
                config['stickers_col_sep']
            ) / config['stickers_columns']
        h = (config['stickers_page_height'] - 2 * config['stickers_top_margin'] -
                (config['stickers_rows'] - 1) * 2 * config['stickers_row_sep']
            ) / config['stickers_rows']
        
        ctx.set_line_width(config['stickers_border_width'])
        ctx.set_source_rgb(*config['stickers_border_color'])
        
        row = 0
        column = 0
        x = config['stickers_hoffset'] + config['stickers_left_margin']
        y = config['stickers_voffset'] + config['stickers_top_margin']
        for q in queries:
            for c in q['q']:
                for d in range(q['count']):
                    if c != (None,):
                        type_name = type(c).__name__.lower()
                        template_name = 'stickers_{}_template'.format(type_name)
                        self.gen_sticker(ctx, c, x=x, y=y, w=w, h=h,
                            font=config['stickers_font'],
                            text_color=config['stickers_text_color'],
                            template=config[template_name])
                    
                    self.next()
                    
                    if self._stop:
                        break
                    
                    x += w + 2 * config['stickers_col_sep']
                    column += 1
                    if column >= config['stickers_columns']:
                        column = 0
                        x = (config['stickers_hoffset'] +
                            config['stickers_left_margin'])
                        row += 1
                        y += h + 2 * config['stickers_row_sep']
                        if row >= config['stickers_rows']:
                            row = 0
                            y = (config['stickers_voffset'] +
                                config['stickers_top_margin'])
                            ctx.get_target().show_page()
                
                if self._stop:
                    break
        
        if row > 0:
            ctx.get_target().show_page()
        
        self._message = 'done'
    
    def gen_sticker(self, ctx, obj, x, y, w, h, font, text_color, template):
        ctx.save()
        
        ctx.rectangle(x, y, w, h)
        ctx.stroke_preserve()
        ctx.clip()
        
        lout = PangoCairo.create_layout(ctx)
        lout.set_font_description(Pango.FontDescription(font))
        lout.set_width(Pango.SCALE * w)
        lout.set_alignment(Pango.Alignment.CENTER)
        
        type_name = type(obj).__name__.lower()
        text = template.format(**{type_name: obj})
        lout.set_markup(text, -1)
        extent = lout.get_size()
        xtrans = x
        ytrans = y - extent.height / Pango.SCALE / 2 + h / 2
        
        ctx.translate(xtrans, ytrans)
        ctx.set_source_rgb(*text_color)
        PangoCairo.update_layout(ctx, lout)
        PangoCairo.show_layout(ctx, lout)
        ctx.translate(-xtrans, -ytrans)
        ctx.restore()
    
    def section_query(self):
        session = self.util.get_scoped_session()
        root_section = self.util.get_root_section(session)
        
        digits = self.util.get_section_digits()
        padding = digits * '0'
        full_number = func.substr(padding + db.Section.number.cast(String),
            -digits, digits)
        icteq = session.query(
                db.Section.id,
                full_number.label('full_number'),
            ).filter_by(
                parent=root_section
            ).cte()
        rcteq = session.query(
                db.Section.id,
                icteq.c.full_number.concat('-').concat(full_number),
            ).join(
                icteq, icteq.c.id == db.Section.parent_id
            )
        cteq = icteq.union(rcteq)
        q = session.query(db.Section).join(
            cteq, db.Section.id == cteq.c.id).order_by(cteq.c.full_number)
        return q
    
    def book_query(self):
        session = self.util.get_scoped_session()
        root_section = self.util.get_root_section(session)
        
        digits = self.util.get_section_digits()
        padding = digits * '0'
        full_number = func.substr(padding + db.Section.number.cast(String),
            -digits, digits)
        icteq = session.query(
                db.Section.id,
                full_number.label('section_full_number'),
            ).filter_by(
                parent=root_section
            ).cte()
        rcteq = session.query(
                db.Section.id,
                icteq.c.section_full_number.concat('-').concat(full_number),
            ).join(
                icteq, icteq.c.id == db.Section.parent_id
            )
        cteq = icteq.union(rcteq)
        
        digits = self.util.get_book_digits()
        padding = digits * '0'
        full_number = cteq.c.section_full_number.concat('-').concat(
            func.substr(padding + db.Book.number.cast(String),
                -digits, digits))
        
        q = session.query(db.Book).join(cteq).order_by(
            cteq.c.section_full_number, db.Book.number)
        return q

