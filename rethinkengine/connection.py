import rethinkdb as r


class Connection(object):
    _conn = None
    _db = None

    @classmethod
    def connect(cls, host, db, port=28015):
        if not cls._conn:
            cls._conn = r.connect(host=host, db=db, port=port)
            cls._conn.use(db)
            cls._db = r.db(db)
        return cls._conn


connect = Connection.connect
