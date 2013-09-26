try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from rethinkengine.connection import get_conn
from rethinkengine.fields import BaseField, PrimaryKeyField
from rethinkengine.query_set import QuerySet, QuerySetManager, DoesNotExist, \
    MultipleObjectsReturned

import inspect
import rethinkdb as r


class ValidationError(Exception):
    pass


class Meta(object):
    order_by = None
    primary_key_field = 'id'


class BaseDocument(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(BaseDocument, cls).__new__(cls, name, bases, attrs)

        # If new_class is of type Document, return straight away
        if object in new_class.__bases__:
            return new_class

        # Process schema
        fields = sorted(
            inspect.getmembers(
                new_class,
                lambda o:isinstance(o, BaseField)
            ),
            key=lambda i:i[1]._creation_order)
        new_class._fields = attrs.get('_fields', OrderedDict())
        new_class._fields['pk'] = PrimaryKeyField()
        for field_name, field in fields:
            new_class._fields[field_name] = field
            delattr(new_class, field_name)
        new_class.objects = QuerySetManager()

        # Merge exceptions
        classes_to_merge = (DoesNotExist, MultipleObjectsReturned)
        for c in classes_to_merge:
            exc = type(c.__name__, (c,), {'__module__': name})
            setattr(new_class, c.__name__, exc)

        # Merge Meta
        m_name = Meta.__name__

        # Get user defined Meta data
        meta_data = {}
        if hasattr(new_class, m_name):
            meta_data = dict([(k, getattr(new_class.Meta, k)) for k in
                dir(new_class.Meta) if not k.startswith('_')])

        # Merge Meta class and set user defined data
        meta = type(m_name, (Meta,), {'__module__': name})
        setattr(new_class, m_name, meta)
        for k, v in meta_data.items():
            setattr(new_class.Meta, k, v)

        # Populate table_name if not privided
        if 'table_name' not in meta_data:
            new_class.Meta.table_name = name.lower()

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
            return self._get_value(key)
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
        return dict([(k, self._get_value(k)) for k in self._fields])

    @classmethod
    def table_create(cls):
        return r.table_create(cls.Meta.table_name,
            primary_key=cls.Meta.primary_key_field).run(get_conn())

    @classmethod
    def table_drop(cls):
        return r.table_drop(cls.Meta.table_name).run(get_conn())

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
        if not self._dirty:
            return True
        self.validate()
        doc = self._doc
        table = r.table(self.Meta.table_name)
        if self.pk:
            # TODO: implement atomic updates instead of updating entire doc
            result = table.get(self.pk).update(doc).run(get_conn())
        else:
            result = table.insert(doc).run(get_conn())
        self._dirty = False
        if 'generated_keys' in result:
            self._data['pk'] = result['generated_keys'][0]
        return True

    def delete(self):
        table = r.table(self.Meta.table_name)
        if self._get_value('pk'):
            return table.get(self._get_value('pk')).delete().run(get_conn())

    def _get_value(self, field_name):
        return self._data.get(field_name, self._fields[field_name]._default)

    @property
    def _doc(self):
        doc = {}
        for name in self._fields:
            key = self.Meta.primary_key_field if name == 'pk' else name
            value = self._get_value(name)
            if key == self.Meta.primary_key_field and value is None:
                continue
            doc[key] = value
        return doc
