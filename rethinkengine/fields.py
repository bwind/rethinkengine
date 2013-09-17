class BaseField(object):
    def __init__(self):
        self._default = None

    def __get__(self, instance, owner):
        return self.to_python()

    def __str__(self):
        return str(self.to_python())

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def to_python(self, value):
        return value


class PrimaryKeyField(BaseField):
    def to_python(self):
        return str(self._value)


class TextField(BaseField):
    def to_python(self, value):
        return str(value)


class ListField(BaseField):
    def __init__(self, value=[]):
        super(ListField, self).__init__()
        self._default = []

    def to_python(self, value):
        return value


class DictField(BaseField):
    pass

