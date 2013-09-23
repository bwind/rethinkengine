from rethinkengine.connection import get_conn
from rethinkengine.fields import BaseField, PrimaryKeyField
from rethinkengine.query_set import QuerySet, QuerySetManager, DoesNotExist, \
    MultipleDocumentsReturned

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
        attrs['_fields']['pk'] = PrimaryKeyField()
        new_class = super(BaseDocument, cls).__new__(cls, name, bases, attrs)
        new_class.objects = QuerySetManager()
        return new_class


class Document(object):
    __metaclass__ = BaseDocument

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__()
        self.__dict__['_data'] = {}
        self.__dict__['_iter'] = None
        self.__dict__['_dirty'] = True
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __setattr__(self, key, value):
        field = self._fields.get(key, None)
        if field is not None:
            if self._get_value(key) != value:
                self._dirty = True
            self._data[key] = value
        super(Document, self).__setattr__(key, value)

    def __getattr__(self, key):
        field = self._fields.get(key)
        if field:
            return self._data.get(key, self._fields[key]._default)
        raise AttributeError

    def __str__(self):
        return '<%s object>' % self.__class__.__name__

    def __iter__(self):
        return self

    def next(self):
        if not self._iter:
            self.__dict__['_iter'] = iter(self._fields)
        return self._iter.next()

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def items(self):
        return dict([(k, self._data.get(k, self._fields[k]._default)) for k in
            self._fields])

    def table_create(self):
        return r.table_create(self._table_name()).run(get_conn())

    def table_drop(self):
        return r.table_drop(self._table_name()).run(get_conn())

    def validate(self):
        data = [(field, getattr(self, name)) for name, field in
            self._fields.items()]
        for field, value in data:
            if isinstance(field, PrimaryKeyField) and value is None:
                continue
            if not field.is_valid(value):
                raise ValidationError('%s is of wrong type %s' %
                    (field.__class__.__name__, type(value)))

    def save(self):
        # TODO: upsert/insert
        if not self._dirty:
            return True
        self.validate()
        doc = self._doc
        table = r.table(self._table_name())
        result = table.insert(doc).run(get_conn())
        self._dirty = False
        if 'generated_keys' in result:
            self._data['pk'] = result['generated_keys'][0]
        return True

    def delete(self):
        table = r.table(self._table_name())
        if self._get_value('pk'):
            return table.get(self._get_value('pk')).delete().run(get_conn())

    def _get_value(self, field_name):
        return self._data.get(field_name, self._fields[field_name]._default)

    @property
    def _doc(self):
        doc = {}
        for name in self._fields:
            key = self.Meta.primary_key_field if name == 'pk' else name
            value = self._data.get(name, self._fields[name]._default)
            if key == self.Meta.primary_key_field and value is None:
                continue
            doc[key] = value
        return doc

    @classmethod
    def _table_name(cls):
        return cls.__name__.lower()

    class Meta:
        order_by = None
        primary_key_field = 'id'
