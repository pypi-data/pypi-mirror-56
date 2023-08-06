# How to import bars without enforcing it as a dependency
try:
    from bars import bars
except ImportError:

    def bars(*args, **kwargs):
        if args:
            return args[0]
        return kwargs.get('iterable', None)
