import re


class BaseField(object):
    def __init__(self):
        # TODO: add 'required' keyword
        self._default = None

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__


class PrimaryKeyField(BaseField):
    rx = r'^[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}$'
    def is_valid(self, value):
        return isinstance(value, basestring) and bool(re.match(self.rx, value))


class StringField(BaseField):
    def __init__(self):
        super(StringField, self).__init__()
        self._default = ''

    def is_valid(self, value):
        return isinstance(value, basestring)


class IntegerField(BaseField):
    def __init__(self):
        super(IntegerField, self).__init__()
        self._default = 0

    def is_valid(self, value):
        return isinstance(value, (int, long))


class FloatField(BaseField):
    def __init__(self):
        super(FloatField, self).__init__()
        self._default = 0.

    def is_valid(self, value):
        return isinstance(value, (float))


class ListField(BaseField):
    def __init__(self):
        super(ListField, self).__init__()
        self._default = []

    def is_valid(self, value):
        return isinstance(value, (list, tuple))


class DictField(BaseField):
    def __init__(self):
        super(DictField, self).__init__()
        self._default = {}

    def is_valid(self, value):
        return isinstance(value, dict)


class BooleanField(BaseField):
    def __init__(self):
        super(BooleanField, self).__init__()
        self._default = None

    def is_valid(self, value):
        return isinstance(value, bool)
