class Singleton(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__()
            cls._instances[cls] = instance
        return cls._instances[cls]
