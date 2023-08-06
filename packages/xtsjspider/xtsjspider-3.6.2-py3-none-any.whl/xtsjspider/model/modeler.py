class Model(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
