from rethinkengine.connection import get_conn
from rethinkengine.fields import PrimaryKeyField

import rethinkdb as r


REPR_SIZE = 20


class InvalidQueryError(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class DoesNotExist(Exception):
    pass


class QuerySet(object):
    def __init__(self, document):
        self._document = document
        self._filter = {}
        self._limit = None
        self._skip = None
        self._count = False
        self._order_by = None
        self._cursor_obj = None
        self._cursor_iter = None
        self._iter_index = 0

    @property
    def _cursor(self):
        if not self._cursor_obj:
            self._build_cursor_obj()
        return self._cursor_iter

    def _build_cursor_obj(self):
        self._cursor_obj = r.table(self._document.Meta.table_name)
        if self._filter:
            self._cursor_obj = self._cursor_obj.filter(self._filter)

        order_by = self._order_by or self._document.Meta.order_by
        if order_by:
            order_by_r = []
            for field in order_by:
                if field.startswith('-'):
                    order_by_r.append(r.desc(field[1:]))
                else:
                    order_by_r.append(r.asc(field))
            self._cursor_obj = self._cursor_obj.order_by(*order_by_r)

        if self._limit:
            self._cursor_obj = self._cursor_obj.limit(self._limit)

        if self._skip:
            self._cursor_obj = self._cursor_obj.skip(self._skip)

        self._iter_index = 0
        self._cursor_iter = iter(self._cursor_obj.run(get_conn()))

    def __getitem__(self, key):
        if isinstance(key, slice):
            self._build_cursor_obj()
            # Get the start, stop, and step from the slice
            return [self[i] for i in xrange(*key.indices(len(self)))]
        elif isinstance(key, int):
            self._build_cursor_obj()
            if key < 0:
                raise AssertionError('Negative indexing is not supported')
            if key >= len(self):
                raise IndexError('List index out of range')
            for i in xrange(key):
                self.next()
            doc = self.next()
            return doc
        else:
            raise TypeError('Invalid argument type')

    def __call__(self):
        return self

    def __iter__(self):
        return self

    def next(self):
        self._iter_index += 1
        doc = self._document()
        doc._dirty = False
        for name, value in self._cursor.next().items():
            if name == self._document.Meta.primary_key_field:
                doc._fields['pk'] = PrimaryKeyField()
                doc._data['pk'] = value
            if name not in doc._fields:
                continue
            # Bypass __setattr__ to prevent _dirty from being set to True
            doc._data[name] = value
        return doc

    def __repr__(self):
        data = []
        for i, doc in enumerate(self):
            data.append(doc)

            if len(data) > REPR_SIZE:
                data[-1] = '.. more objects ..'
                break

        return repr(data)

    def all(self):
        return self.__call__()

    def filter(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._filter:
                message = "Encountered '%s' more than once in query" % k
                raise InvalidQueryError(message)
            elif k == 'pk':
                k = self._document.Meta.primary_key_field
            self._filter[k] = v
        return self.__call__()

    def get(self, **kwargs):
        self.filter(**kwargs)
        self._limit = 2
        try:
            doc1 = self.next()
        except StopIteration:
            message = 'Query did not match any %s objects' % \
                self._document.__name__
            raise self._document.DoesNotExist(message)
        try:
            doc2 = self.next()
        except StopIteration:
            return doc1
        message = 'Query returned more than 1 %s object' % \
            self._document.__name__
        raise self._document.MultipleObjectsReturned(message)

    def get_or_create(self, **kwargs):
        # Shorthand function for either getting a document, and if it doesn't
        # exist, creating it.
        try:
            doc = self._document.objects.get(**kwargs)
            created = False
        except DoesNotExist:
            doc = self.create(**kwargs)
            created = True
        return created, doc

    def create(self, **kwargs):
        doc = self._document(**kwargs)
        doc.save()
        return doc

    def __len__(self):
        if not self._cursor_obj:
            self._build_cursor_obj()
        return self._cursor_obj.count().run(get_conn())

    def limit(self, limit):
        self._limit = limit
        return self.__call__()

    def skip(self, skip):
        self._skip = skip
        return self.__call__()

    def order_by(self, *args):
        self._order_by = args
        return self.__call__()

    def delete(self):
        self._build_cursor_obj()
        for doc in self:
            doc.delete()


class QuerySetManager(object):
    def __get__(self, instance, owner):
        # Returns a new QuerySet instance when Document.objects is accessed
        return QuerySet(document=owner)
