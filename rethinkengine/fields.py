import re


class BaseField(object):
    _creation_counter = 0
    def __init__(self, required=True, default=None):
        self._creation_order = self._creation_counter
        BaseField._creation_counter += 1
        self._required = required
        self._default = default

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def is_valid(self, value):
        if not self._required and value is None:
            return True
        return False


class PrimaryKeyField(BaseField):
    rx = r'^[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}$'

    def __init__(self):
        # PrimaryKeyField.__init__ doesn't accept any arguments
        self._default = None

    def is_valid(self, value):
        return isinstance(value, basestring) and bool(re.match(self.rx, value))


class StringField(BaseField):
    def is_valid(self, value):
        if super(StringField, self).is_valid(value) is True:
            return True
        return isinstance(value, basestring)


class IntegerField(BaseField):
    def is_valid(self, value):
        if super(IntegerField, self).is_valid(value) is True:
            return True
        return isinstance(value, (int, long))


class FloatField(BaseField):
    def is_valid(self, value):
        if super(FloatField, self).is_valid(value) is True:
            return True
        return isinstance(value, (float))


class ListField(BaseField):
    def is_valid(self, value):
        if super(ListField, self).is_valid(value) is True:
            return True
        return isinstance(value, (list, tuple))


class DictField(BaseField):
    def is_valid(self, value):
        if super(DictField, self).is_valid(value) is True:
            return True
        return isinstance(value, dict)


class BooleanField(BaseField):
    def is_valid(self, value):
        if super(BooleanField, self).is_valid(value) is True:
            return True
        return isinstance(value, bool)
