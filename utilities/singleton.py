class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = None
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            # cls._instances[cls].__constructor__(*args)
        return cls._instances[cls]
