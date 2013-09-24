import re


class BaseField(object):
    def __init__(self, required=True):
        self._required = required
        self._default = None

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def is_valid(self, value):
        if not self._required and value is None:
            return True
        return False


class PrimaryKeyField(BaseField):
    rx = r'^[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}$'
    def is_valid(self, value):
        return isinstance(value, basestring) and bool(re.match(self.rx, value))


class StringField(BaseField):
    def __init__(self, **kwargs):
        super(StringField, self).__init__(**kwargs)
        self._default = ''

    def is_valid(self, value):
        if super(StringField, self).is_valid(value) is True:
            return True
        return isinstance(value, basestring)


class IntegerField(BaseField):
    def __init__(self, **kwargs):
        super(IntegerField, self).__init__(**kwargs)
        self._default = 0

    def is_valid(self, value):
        if super(IntegerField, self).is_valid(value) is True:
            return True
        return isinstance(value, (int, long))


class FloatField(BaseField):
    def __init__(self, **kwargs):
        super(FloatField, self).__init__(**kwargs)
        self._default = 0.

    def is_valid(self, value):
        if super(FloatField, self).is_valid(value) is True:
            return True
        return isinstance(value, (float))


class ListField(BaseField):
    def __init__(self, **kwargs):
        super(ListField, self).__init__(**kwargs)
        self._default = []

    def is_valid(self, value):
        if super(ListField, self).is_valid(value) is True:
            return True
        return isinstance(value, (list, tuple))


class DictField(BaseField):
    def __init__(self, **kwargs):
        super(DictField, self).__init__(**kwargs)
        self._default = {}

    def is_valid(self, value):
        if super(DictField, self).is_valid(value) is True:
            return True
        return isinstance(value, dict)


class BooleanField(BaseField):
    def __init__(self, **kwargs):
        super(BooleanField, self).__init__(**kwargs)
        self._default = None

    def is_valid(self, value):
        if super(BooleanField, self).is_valid(value) is True:
            return True
        return isinstance(value, bool)
