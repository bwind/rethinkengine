class BaseField(object):
    def __init__(self):
        # TODO: add 'required' keyword
        self._default = None

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def to_python(self, value):
        return value


class PrimaryKeyField(BaseField):
    def is_valid(self, value):
        return isinstance(value, basestring)


class TextField(BaseField):
    def __init__(self):
        super(TextField, self).__init__()
        self._default = ''

    def is_valid(self, value):
        return isinstance(value, basestring)


class IntegerField(BaseField):
    def __init__(self):
        super(IntegerField, self).__init__()
        self._default = 0

    def is_valid(self, value):
        return isinstance(value, (int, long))


class ListField(BaseField):
    def __init__(self):
        super(ListField, self).__init__()
        self._default = []

    def to_python(self, value):
        return value

    def is_valid(self, value):
        return isinstance(value, (list, tuple))


class DictField(BaseField):
    def __init__(self):
        super(DictField, self).__init__()
        self._default = {}

    def is_valid(self, value):
        return isinstance(value, dict)
