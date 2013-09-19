import rethinkdb as r


DEFAULT_DATABASE_NAME = 'default'


get_alias = lambda d: d or ConnectionManager._active_alias or DEFAULT_DATABASE_NAME


class ConnectionError(Exception):
    pass


class ConnectionManager(object):
    _connections = {}
    _active_alias = None

    @classmethod
    def connect(cls, db=None, alias=None, host='localhost', port=28015):
        db = get_alias(db)
        alias = alias or db
        if alias not in cls._connections:
            cls._connections[alias] = r.connect(host=host, db=db, port=port)
            cls._active_alias = alias
        return cls._connections[alias]

    @classmethod
    def disconnect(cls, alias=None):
        alias = get_alias(alias)
        if not alias or alias not in cls._connections:
            raise ConnectionError('Not connected')
        cls.get_conn(alias=alias).close()
        cls._active_alias = None
        del cls._connections[alias]

    @classmethod
    def get_conn(cls, alias=None):
        alias = get_alias(alias)
        if alias not in cls._connections:
            raise ConnectionError('No such connection')
        return cls.connect(alias=alias)


connect, disconnect, get_conn = (ConnectionManager.connect,
                                 ConnectionManager.disconnect,
                                 ConnectionManager.get_conn)
