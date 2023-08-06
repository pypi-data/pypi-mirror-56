__path__ = __import__('pkgutil').extend_path(__path__, __name__)

try:
    from .__doc__ import __doc__
except ImportError:
    pass
