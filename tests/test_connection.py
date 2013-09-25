from . import DB_NAME
from random import choice
from rethinkengine.connection import *
from string import ascii_letters

import rethinkdb
import rethinkengine.connection
import unittest2 as unittest


class ConnectionTestCase(unittest.TestCase):
    def test_connect(self):
        # Assert whether connect() returns an instance of
        # rethinkdb.net.Connection
        conn = connect(DB_NAME)
        self.assertIsInstance(conn, rethinkdb.net.Connection)

    def test_connect_db_does_not_exist(self):
        db_name = DB_NAME + ''.join(choice(ascii_letters) for i in range(6))
        conn = connect(db_name)
        self.assertIsInstance(conn, rethinkdb.net.Connection)
        # Clean up
        db_drop(db_name)

    def test_drop_db(self):
        db_name = DB_NAME + ''.join(choice(ascii_letters) for i in range(6))
        conn = connect(db_name)
        self.assertIn(db_name, db_list())
        db_drop(db_name)
        # Make sure the db does not exist anymore
        self.assertNotIn(db_name, db_list())

    def test_connect_wrong_port(self):
        with self.assertRaises(ConnectionError):
            # We'll just assume that RethinkDB is not running on port 11111
            connect(port=11111)

    def test_disconnect(self):
        # Assert that a disconnect() doesn't raise an error when connected
        connect(DB_NAME)
        disconnect(DB_NAME)

    def test_get_conn(self):
        # Assert whether get_conn() returns an instance of
        # rethinkdb.net.Connection
        connect(DB_NAME)
        self.assertIsInstance(get_conn(), rethinkdb.net.Connection)

    def test_get_conn_raises(self):
        # Assert whether get_conn() raises an error when not connected
        connect()
        disconnect()
        self.assertRaises(ConnectionError, get_conn)

    def test_disconnect_raises(self):
        # Assert whether a disconnect raises a ConnectionError when
        # not connected
        self.assertRaises(ConnectionError, disconnect, (DB_NAME))

    def test_connect_default(self):
        # Assert wheter connect() uses DEFAULT_DATABASE_NAME, even after
        # having connected and disconnected to a different db name
        db_name = DB_NAME + ''.join(choice(ascii_letters) for i in range(6))
        connect(db_name)
        # Clean up
        db_drop(db_name)
        disconnect(db_name)
        conn = connect()
        self.assertEqual(conn.db, rethinkengine.connection.DEFAULT_DATABASE_NAME)
        disconnect()

    def test_disconnect_active_alias(self):
        # Assert whether disconnect() uses the active alias (and doesn't raise
        # a ConnectionError)
        db_name = DB_NAME + ''.join(choice(ascii_letters) for i in range(6))
        connect(db_name)
        # Clean up
        db_drop(db_name)
        disconnect()

    def test_disconnect_with_alias(self):
        # Assert whether disconnect() works when using an alias
        alias = DB_NAME + ''.join(choice(ascii_letters) for i in range(6))
        connect(DB_NAME, alias=alias)
        disconnect(alias)
