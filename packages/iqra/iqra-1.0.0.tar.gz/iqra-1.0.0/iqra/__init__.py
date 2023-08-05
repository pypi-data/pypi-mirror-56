'''
:Date: 2019-11-18
:Version: 1.0.0
:Authors:
    * Mohammad Alghafli <thebsom@gmail.com>

Iqra, a library management program.
This is the core iqra library. It also acts as a commandline interface to interact with iqra database with basic commands.
If you are looking for a GUI library management program, look for giqra which provides a user interface to interact with iqra database.

------------
Installation
------------

On windows install using pip by running the
command::
    
    pip install iqra

Or on linux::
    
    pip3 install iqra

All dependancies will be installed automatically by pip. The stickers plugin needs pycairo so you need to install it if you want to use this plugin.

-----
Usage
-----

Running the commandline interface::

    python3 -m iqra

Use -h option to know all the possible options::

    python3 -m iqra -h

You can use iqra as a library and import it in your project::

    import iqra
'''

import json
import threading
import logging
from . import db
import traceback
import appdirs
import codi
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy.event
import os
import cmd
import pkg_resources
import shlex
import argparse
import datetime
import shutil

try:
    import cairo
    import gi
    gi.require_version('Pango', '1.0')
    gi.require_version('PangoCairo', '1.0')
    
    from gi.repository import Pango
    from gi.repository import PangoCairo
except ImportError:
    cairo = None

__version__ = '1.0.0'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

class IqraUtil:
    CONFIG = {
            'library_name': 'Library',
            'language': 'en',
            'backup_count': 10,
            'section_digits': 0,
            'book_digits': 0,
        }
    
    def __init__(self, config_dir=None, profile='default'):
        global _
        
        dbname = 'library_{}.db'.format(__version__.split('.')[0])
        
        config_dirs = [pathlib.Path(__file__).parent]
        if config_dir is not None:
            p = pathlib.Path(config_dir)
            config_dirs.insert(0, p / profile)
        else:
            portable_config = pathlib.Path(__file__).parent / 'iqra.cfg'
            if not portable_config.exists():
                p = pathlib.Path(appdirs.user_config_dir('iqra', 'mhghafli'))
                config_dirs.insert(0, p / profile)
        
        self.codi = codi.Codi(*config_dirs)
        
        self.new_config = False
        self.config = codi.Config()
        self.add_default_config(self.CONFIG)
        self.config.update(self.load_config())
        
        self.dbpath = self.codi.path(dbname, writable=True)
        dburi = 'sqlite:///{}'.format(self.dbpath)
        self.engine = create_engine(dburi, isolation_level=None, echo=False)
        sqlalchemy.event.listen(self.engine, 'begin', self.on_engine_begin)
        
        db.Base.metadata.create_all(self.engine)
        
        self.Sessionmaker = sessionmaker(bind=self.engine)
        self.Scopedmaker = scoped_session(sessionmaker(bind=self.engine))
        
        self.create_root_section()
        
        self.language = self.get_config('language')
        os.putenv('LANGUAGE', self.language)
    
    def create_root_section(self):
        session = self.get_session()
        
        if session.query(db.Section).filter_by(parent_id=None).count() < 1:
            section = db.Section(
                id=0, parent_id=None, number=0, name='', abbreviation='')
            session.add(section)
            session.commit()
        
        if session.query(db.Section).filter_by(parent_id=None).count() > 1:
            for c in session.query(db.Section).filter_by(section_id=None).offset(1):
                session.delete(c)
            
            session.commit()
        
        session.close()
    
    def get_root_section(self, session):
        return session.query(db.Section).get(0)
    
    def get_section(self, session, *numbers):
        section = self.get_root_section(session)
        for c in numbers:
            section = session.query(db.Section).filter_by(
                parent=section, number=c).one()
        return section
    
    def get_books(self, session, *numbers, columns=[db.Book]):
        section = self.get_section(session, *numbers[:-1])
        q = session.query(*columns).filter_by(
            section=section, number=numbers[-1])
        return q
    
    def backup(self):
        budir = self.get_path('backup', True)
        try:
            budir.mkdir(parents=True)
        except FileExistsError:
            pass
        dt = datetime.datetime.now()
        dest = budir / '{:%Y%m%d_%H%M%S}.db'.format(dt)
        
        conn = self.engine.connect()
        conn.execute('BEGIN IMMEDIATE TRANSACTION')
        shutil.copy2(str(self.dbpath), str(dest))
        conn.execute('ROLLBACK')
        conn.close()
        
        backups = self.list_backups()
        to_delete = len(backups) - self.get_config('backup_count')
        if to_delete > 0:
            to_remove = backups[:to_delete]
            for c in to_remove:
                c.unlink()
    
    def list_backups(self):
        return sorted([c for c in self.glob_path('backup/*.db') if c.is_file()])
    
    def restore(self, backup=None):
        backups = self.list_backups()
        if backup is None:
            backup = backups[-1].stem
        
        try:
            backup = [c for c in backups if c.stem == backup][0]
        except IndexError:
            raise FileNotFoundError('backup file does not exist')
        v = __version__.split('.')[0]
        dest = self.dbpath
        shutil.copy2(str(backup), str(self.dbpath))
    
    def on_engine_begin(self, conn):
        conn.execute('BEGIN')
    
    def add_default_config(self, def_conf):
        for c in def_conf:
            try:
                self.config.get_default(c)
            except KeyError:
                self.config.set_default(c, def_conf[c])
    
    def load_config(self):
        try:
            return json.loads(self.codi.read('iqra.cfg'))
        except Exception as e:
            if type(e) is not FileNotFoundError:
                print('error loading config')
                print(e)
                print(traceback.format_exc())
                print('will create new config')
            
            self.new_config = True
            self.codi.write('iqra.cfg', json.dumps({}))
            
            return {}
    
    def dump_config(self):
        try:
            self.codi.write('iqra.cfg', json.dumps(self.config))
        except Exception as e:
            logger.warning('could not write config file. Error: {} `{}`'.format(
                type(e).__name__, e))
    
    def get_config_names(self):
        return sorted(self.config)
    
    def get_config(self, name):
        return self.config[name]
    
    def set_config(self, name, value):
        self.config[name] = value
    
    def get_path(self, fpath, writable=False):
        return self.codi.path(fpath, writable)
    
    def glob_path(self, pattern):
        return self.codi.glob(pattern)
    
    def get_session(self, *args, **kwargs):
        return self.Sessionmaker(*args, **kwargs)
    
    def get_scoped_session(self, *args, **kwargs):
        session = self.Scopedmaker(*args, **kwargs)
        return session
    
    def get_commands(self):
        return pkg_resources.iter_entry_points('iqra.commands')
    
    def get_plugins(self, name=None):
        plugins = [
            c.load() for c in pkg_resources.iter_entry_points(
                'iqra.plugins', name)
        ]
        
        for c in plugins:
            try:
                self.add_default_config(c.CONFIG)
            except AttributeError:
                pass
        return plugins
    
    def get_section_digits(self):
        digits = self.get_config('section_digits')
        if digits <= 0:
            digits = self.find_section_digits()
        
        return digits
    
    def find_section_digits(self):
        session = self.get_scoped_session()
        q = session.query(db.Section.number).order_by(
            db.Section.number.desc())
        obj = q.first()
        if obj is not None:
            digits = len(str(obj[0]))
        else:
            digits = 1
        
        return digits
    
    def get_book_digits(self):
        digits = self.get_config('book_digits')
        if digits <= 0:
            digits = self.find_book_digits()
        
        return digits
    
    def find_book_digits(self):
        session = self.get_scoped_session()
        q = session.query(db.Book.number).order_by(db.Book.number.desc())
        obj = q.first()
        if obj is not None:
            digits = len(str(obj[0]))
        else:
            digits = 1
        
        return digits
    
    def get_thumbs(self, id):
        return self.glob_path('res/thumbs/{}.*'.format(id))
    
    def delete_thumb(self, id):
        for c in self.get_thumbs(id):
            c.unlink()
    
    def set_thumb(self, id, thumb):
        thumb = pathlib.Path(thumb)
        thumbs_dir = self.get_path('res/thumbs/', writable=True).mkdir(
            parents=True, exist_ok=True)
        thumb_path = self.get_path(
            'res/thumbs/{}{}'.format(id, thumb.suffix), writable=True)
        if thumb != thumb_path:
            shutil.copy(str(thumb), str(thumb_path))
        
        to_delete = [c for c in self.get_thumbs(id) if c != thumb_path]
        for c in to_delete:
            c.unlink()
    
    def add_electronic_file(self, id, path):
        print('adding', path)
        path = pathlib.Path(path)
        e_dir = self.get_path('res/electronic/', writable=True).mkdir(
            parents=True, exist_ok=True)
        e_path = self.get_path(
            'res/electronic/{}{}'.format(id, path.suffix), writable=True)
        if path != e_path:
            shutil.copy(str(path), str(e_path))
    
    def delete_electronic_file(self, id, ext):
        e_path = self.get_path(
            'res/electronic/{}{}'.format(id, ext), writable=True)
        e_path.unlink()
    
    def get_electronic_files(self, id):
        return self.glob_path('res/electronic/{}.*'.format(id))
    
    def generate_thumb(self, book):
        if cairo is None:
            raise RuntimeError('cairo library is missing. must install it.')
        
        H = 128
        W = 128
        LINE_WIDTH = 4
        TEMPLATE = '{.title}'
        
        if type(book) is int:
            book = self.get_scoped_session().query(db.Book).get(book)
        
        path = self.get_path('res/thumbs/{}.svg'.format(book.id),
            writable=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        surface = cairo.SVGSurface(str(path), W, H)
        
        ctx = cairo.Context(surface)
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        
        ctx.set_line_width(LINE_WIDTH)
        x = y = LINE_WIDTH / 2
        w = W - LINE_WIDTH
        h = H - LINE_WIDTH
        ctx.rectangle(x, y, w, h)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke_preserve()
        ctx.clip()
        
        lout = PangoCairo.create_layout(ctx)
        lout.set_font_description(Pango.FontDescription('Sans 10'))
        lout.set_width(Pango.SCALE * w)
        lout.set_alignment(Pango.Alignment.CENTER)
        
        text = TEMPLATE.format(book)
        lout.set_markup(text, -1)
        extent = lout.get_size()
        xtrans = x
        ytrans = y - extent.height / Pango.SCALE / 2 + h / 2
        
        ctx.translate(xtrans, ytrans)
        PangoCairo.update_layout(ctx, lout)
        PangoCairo.show_layout(ctx, lout)
        
        surface.finish()
        
        return path

class IqraCmd(cmd.Cmd):
    prompt = '>>> '
    
    def __init__(self, util=None, plugins=None, commands=None, *args, **kwargs):
        if util is None:
            util = IqraUtil()
        
        if plugins is None:
            plugins = util.get_plugins()
        
        if commands is None:
            commands = [c.load() for c in util.get_commands()]
        
        self.util = util
        self.session = util.get_session()
        
        self.parser = argparse.ArgumentParser(prog='', add_help=False,
            description='iqra, a library management program')
        
        parsers = self.parser.add_subparsers()
        
        self.commands = set()
        
        self.add_plugins(parsers, plugins)
        self.add_commands(parsers, commands, top_commands=True)
        
        if not hasattr(type(self), 'intro'):
            type(self).intro = 'welcome to {}'.format(
                self.util.get_config('library_name')
            )
        
        super().__init__(*args, **kwargs)
    
    def do_exit(self, arg):
        '''end command line program.'''
        return True
    
    def do_EOF(self, arg):
        '''end command line program.'''
        print()
        return self.do_exit(arg)
    
    def cmdloop(self, *args, **kwargs):
        while True:
            try:
                super().cmdloop()
                break
            except Exception as e:
                print(e)
                print(traceback.format_exc())
    
    def emptyline(self):
        pass
    
    def default(self, arg):
        self.execute_line(arg)
    
    def execute_line(self, args):
        if type(args) is str:
            args = shlex.split(args)
        try:
            ns = vars(self.parser.parse_args(args))
            ns.pop('func')(**ns)
        except SystemExit:
            pass
    
    def add_plugins(self, parsers, plugins):
        for c in plugins:
            if hasattr(c, 'name'):
                name = c.name
            else:
                name = c.__name__
            parser = parsers.add_parser(name, prog=name, description=c.__doc__, **c.parser_args)
            
            cmd_method = 'do_{}'.format(name)
            cmd_help = 'help_{}'.format(name)
            self.commands.add(cmd_method)
            self.commands.add(cmd_help)
            setattr(self, cmd_help, parser.print_help)
            
            caller = PluginCaller(c, util=self.util)
            parser.set_defaults(func=caller.call)
            
            for args in c.args:
                parser.add_argument(*args[0], **args[1])
    
    def add_commands(self, parsers, commands, top_commands=False):
        for c in commands:
            if hasattr(c, 'name'):
                name = c.name
            else:
                name = c.__name__
            parser = parsers.add_parser(name, prog=name, description=c.__doc__, **c.parser_args)
            
            if top_commands:
                cmd_method = 'do_{}'.format(name)
                cmd_help = 'help_{}'.format(name)
                self.commands.add(cmd_method)
                self.commands.add(cmd_help)
                setattr(self, cmd_help, parser.print_help)
            
            parser.set_defaults(func=c(util=self.util).call)
            
            for args in c.args:
                parser.add_argument(*args[0], **args[1])
            
            if hasattr(c, 'subcommands'):
                subparsers = parser.add_subparsers()
                self.add_commands(subparsers, c.subcommands)
    
    def get_names(self):
        return sorted(dir(type(self)) + list(self.commands))

class PluginCaller:
    def __init__(self, plugin_cls, util=None):
        if util is None:
            util = IqraUtil()
        
        self.util = util
        self.plugin = plugin_cls(util=self.util, close=False)
        self.stopped = threading.Event()
        self.stopped.set()
    
    def call(self, *args, **kwargs):
        self.stopped.clear()
        cancelled = False
        t = threading.Thread(target=self.print_info, daemon=True)
        t.start()
        try:
            self.plugin.call(*args, **kwargs)
        except KeyboardInterrupt:
            cancelled = True
        finally:
            self.stopped.set()
        
        t.join(0.1)
        if cancelled:
            print('cancelled')
        else:
            print()
    
    def print_info(self):
        message_length = 0
        while not self.stopped.wait(timeout=0.1):
            message = self.get_info()
            print(message.ljust(message_length), end='', flush=True)
            message_length = len(message)
        
        message = self.get_info()
        print(message.ljust(message_length), end='', flush=True)
    
    def get_info(self):
        finished = self.plugin.finished
        total = self.plugin.total
        digits = str(len(str(total)))
        message = self.plugin.message
        base_str = '\r{:><digits>}/{}'.replace('<digits>', digits)
        progress = base_str.format(finished,total)
        return '{} {}'.format(progress, message)

