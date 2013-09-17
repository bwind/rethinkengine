from rethinkengine.connection import Connection
from rethinkengine.fields import BaseField, PrimaryKeyField
from rethinkengine.queryset import QuerySet

import rethinkdb as r


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

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__()
        self.__dict__['_data'] = {}
        if '_doc' in kwargs:
            for name, value in kwargs['_doc'].items():
                if name == 'id':
                    self._fields['pk'] = PrimaryKeyField()
                    self._data['pk'] = value
                if name not in self._fields:
                    continue
                self._data[name] = value
        else:
            for name, value in kwargs.items():
                if name not in self._fields:
                    continue
                self._data[name] = value

    def __setattr__(self, key, value):
        if key in self._data:
            self._data[key] = value
        super(Document, self).__setattr__(key, value)

    def __getattr__(self, key):
        if key in self._fields:
            return self._data.get(key, self._fields[key]._default)
        super(Document, self).__getattr__(key)

    def __str__(self):
        return '<%s object>' % self.__class__.__name__

    def __iter__(self):
        for name in self._fields:
            yield name

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def items(self):
        return [(k, self._data.get(k, self._fields[k]._default)) for k in self._fields]

    def table_create(self):
        return Connection._db.table_create(self._table_name()).run(Connection._conn)

    def save(self):
        return Connection._db.table(self._table_name()).insert(self._doc).run(Connection._conn)

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
