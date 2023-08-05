from . import IqraUtil

class IqraCommand:
    'iqra command base class. should be inherited'
    
    parser_args = {}
    
    args = tuple()
    
    def __init__(self, util=None):
        if util is None:
            util = IqraUtil()
        
        self.util = util
    
    @classmethod
    def call(cls, **kwargs):
        cls.help()
    
    @classmethod
    def help(cls):
        print('specify a subcommand:')
        for c in cls.subcommands:
            if hasattr(c, 'description'):
                print('    {}: {}'.format(c.__name__, c.description))
            else:
                print('    {}'.format(c.__name__))

class IqraPlugin:
    'iqra plugin base class. should be inherited'
    
    parser_args = {}
    
    def __init__(self, util=None, close=True, start=None, step=None, end=None):
        if util is None:
            util = IqraUtil()
        
        self.util = util
        self.close = close
        self._finished = -1
        self._total = -1
        self._message = ''
        self._stop = False
        self.start = start
        self.step = step
        self.end = end
        
        if self.step is not None:
            self.next = self.callback_next
        else:
            self.next = self.normal_next
    
    @property
    def finished(self):
        return self._finished
    
    def callback_next(self):
        self._finished += 1
        if self.step is not None:
            self.step(self)
    
    def normal_next(self):
        self._finished += 1
    
    @property
    def total(self):
        return self._total
    
    @property
    def message(self):
        return self._message
    
    @property
    def ratio(self):
        if self.total <= 0:
            return -1
        elif self.total == self.finished:
            return 1
        else:
            return self.finished / self.total
    
    @property
    def percentage(self):
        return 100 * self.ratio
    
    def stop(self):
        self._stop = True
    
    def call(self, *args, **kwargs):
        if self.start is not None:
            self.start(self)
        session = self.util.get_scoped_session()
        session.begin_nested()
        try:
            self.do_call(*args, **kwargs)
            session.commit()
            if self.close:
                session.commit()
            if self.end is not None:
                self.end(self)
        except Exception:
            raise
        finally:
            session.close()
    
    def do_call(self, *args, **kwargs):
        raise NotImplemented('this method should be overridden in a subclass.')

