"""
Singleton base class.
"""


class _Singleton(type):
    """
    A metaclass that creates a Singleton base class when called.
    """
    _instances = {}
    verbose = False
    is_initialized = False

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls].verbose = False
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass
