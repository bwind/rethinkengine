from rethinkengine.connection import Connection

import rethinkdb as r


REPR_SIZE = 20


class InvalidQueryError(Exception):
    pass


class QuerySet(object):
    def __init__(self):
        self._filter = {}
        self._order_by = None
        self._cursor_obj = None

    @property
    def _cursor(self):
        if not self._cursor_obj:
            self._cursor_obj = Connection._db.table(self._document._table_name())

            if self._filter:
                self._cursor_obj = self._cursor_obj.filter(self._filter)

            if self._order_by:
                self._cursor_obj = self._cursor_obj.order_by(self._order_by)

        return self._cursor_obj.run(Connection._conn)

    def __get__(self, instance, owner):
        self._document = owner
        return self

    def __call__(self):
        return self

    def __iter__(self):
        for doc in self._cursor:
            yield self._document(_doc=doc)

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

    def filter(self, **query):
        for k, v in query.items():
            if k in self._filter:
                raise InvalidQueryError("Encountered '%s' more than once in query" % k)
            self._filter[k] = v
        return self

    def exclude(self):
        pass

    def get(self):
        pass

    def get_or_create(self):
        pass

    def create(self):
        pass

    def __len__(self):
        pass

    def limit(self):
        pass

    def skip(self):
        pass

    def order_by(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
