
noPrint = lambda *a, **kw:None
class MetaDebug(type):
    _mode = False
    print = noPrint
    @property
    def mode(cls):
        return cls._mode
    @mode.setter
    def mode(cls, value):
        cls._mode = value
        cls.print = print if value else noPrint

class debug(metaclass=MetaDebug):
    """
    Usages:
    [1] Everytime the function get called the messages get printed if debug.mode is True

        @debug(bf, af)      # bf is the message to say before running the function, af is the message to say after 
        def yourFunction(*args, **kw):
            ...

    [2] you can do the same inside your function with debug.print

        def yourFunction(*args, **kw):
            ...
            debug.print("Doing Stuff...")
            ...

    To Enable/Disable the debug mode use respectively, the default is False:

        debug.setOn()
        debug.setOff()
    """
    @classmethod
    def turnOn(cls):
        cls.mode = True
    @classmethod
    def turnOff(cls):
	cls.mode = False

    def __init__(self, bf="",af=""):
        self.bf = bf
        self.af = af


    def __call__(self, func):
        return self.wrap(func)

    def wrap(self, func):
        def function(*args, **kwargs):
            self.print(self.bf)
            return func(*args, **kwargs)
	    self.print(self.af)
        return function



