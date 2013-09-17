from rethinkengine.connection import Connection
from rethinkengine.fields import BaseField, PrimaryKeyField
from rethinkengine.queryset import QuerySet, DoesNotExist, MultipleDocumentsReturned

import rethinkdb as r


class ValidationError(Exception):
    pass


class BaseDocument(type):
    def __new__(cls, name, bases, attrs):
        attrs['_fields'] = attrs.get('_fields', {})
        for field_name, field in attrs.items():
            if not isinstance(field, BaseField):
                continue
            attrs['_fields'][field_name] = field
            del attrs[field_name]
        new_class = super(BaseDocument, cls).__new__(cls, name, bases, attrs)
        new_class.objects = QuerySet()
        return new_class


class Document(object):
    __metaclass__ = BaseDocument

    def __init__(self, _doc=None, *args, **kwargs):
        super(Document, self).__init__()
        self.__dict__['_data'] = {}
        if _doc is not None:
            for name, value in _doc.items():
                if name == self.Meta.primary_key_field:
                    self._fields['pk'] = PrimaryKeyField()
                    self._data['pk'] = value
                if name not in self._fields:
                    continue
                setattr(self, name, value)
        else:
            for name, value in kwargs.items():
                setattr(self, name, value)

    def __setattr__(self, key, value):
        field = self._fields.get(key, None)
        if field is None:
            raise AttributeError
        valid = field.is_valid(value)
        if valid:
            self._data[key] = value
        else:
            raise ValidationError
        super(Document, self).__setattr__(key, value)

    def __getattr__(self, key):
        field = self._fields.get(key)
        if field:
            return self._data.get(key, self._fields[key]._default)
        raise AttributeError

    def __str__(self):
        return '<%s object>' % self.__class__.__name__

    def __iter__(self):
        for name in self._fields:
            yield name

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def items(self):
        return [(k, self._data.get(k, self._fields[k]._default)) for k in
            self._fields]

    def table_create(self):
        return Connection._db.table_create(self._table_name()).run(Connection._conn)

    def validate(self):
        data = [(field, getattr(self, name)) for name, field in self._fields.items()]
        for field, value in data:
            if not field.is_valid(value):
                raise ValidationError

    def save(self):
        # TODO: only save if doc changed
        # TODO: upsert/insert
        self.validate()
        return Connection._db.table(self._table_name()).insert(self._doc
            ).run(Connection._conn)

    @property
    def _doc(self):
        doc = {}
        for name in self._fields:
            key = self.Meta.primary_key_field if name == 'pk' else name
            doc[key] = self._data.get(name, self._fields[name]._default)
        return doc

    @classmethod
    def _table_name(cls):
        return cls.__name__.lower()

    class Meta:
        order_by = None
        primary_key_field = 'id'
