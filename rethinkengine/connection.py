import rethinkdb as r


DEFAULT_DATABASE_NAME = 'default'

_connections = {}
_active_alias = None


class ConnectionError(Exception):
    pass


# Shorthand function to fall back on either the last used db, or default
get_alias = lambda d: d or _active_alias or DEFAULT_DATABASE_NAME


def connect(db=None, alias=None, host='localhost', port=28015):
    global _connections
    global _active_alias
    # No value for 'db' means _active_alias (last used), or default.
    db = get_alias(db)
    # If alias isn't provided, use db
    alias = alias or db
    if alias not in _connections:
        try:
            _connections[alias] = r.connect(host=host, db=db, port=port)
        except r.RqlDriverError:
            raise ConnectionError('Could not connect to %s:%d/%s' %
                (host, port, db))
        if db not in db_list(alias):
            db_create(db, alias)
        _connections[alias].use(db)
        _active_alias = alias
    return _connections[alias]

def disconnect(alias=None):
    global _connections
    global _active_alias
    alias = get_alias(alias)
    if not alias or alias not in _connections:
        raise ConnectionError('Not connected')
    get_conn(alias=alias).close()
    _active_alias = None
    del _connections[alias]

def get_conn(alias=None):
    global _connections
    alias = get_alias(alias)
    if alias not in _connections:
        raise ConnectionError('No such connection')
    return connect(alias=alias)

def db_list(alias=None):
    return r.db_list().run(get_conn(alias))

def db_create(db, alias=None):
    alias = alias or db
    conn = get_conn(alias)
    r.db_create(db).run(conn)

def db_drop(db, alias=None):
    alias = alias or db
    conn = get_conn(alias)
    r.db_drop(db).run(conn)
