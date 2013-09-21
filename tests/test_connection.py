from rethinkengine.connection import connect, disconnect, get_conn, \
    ConnectionError

import rethinkdb
import rethinkengine.connection
import unittest2 as unittest


class ConnectionTestCase(unittest.TestCase):
    def setUp(self):
        self.db_name = 'test'

    def tearDown(self):
        try:
            disconnect(self.db_name)
        except ConnectionError:
            pass
        try:
            disconnect()
        except ConnectionError:
            pass

    def test_connect(self):
        # Assert whether connect() returns an instance of
        # rethinkdb.net.Connection
        conn = connect(self.db_name)
        self.assertIsInstance(conn, rethinkdb.net.Connection)

    def test_disconnect(self):
        # Assert that a disconnect() doesn't raise an error when connected
        connect(self.db_name)
        disconnect(self.db_name)

    def test_get_conn(self):
        # Assert whether get_conn() returns an instance of
        # rethinkdb.net.Connection
        connect(self.db_name)
        self.assertIsInstance(get_conn(), rethinkdb.net.Connection)

    def test_get_conn_raises(self):
        # Assert whether get_conn() raises an error when not connected
        self.assertRaises(ConnectionError, get_conn)

    def test_disconnect_raises(self):
        # Assert whether a disconnect raises a ConnectionError when
        # not connected
        self.assertRaises(ConnectionError, disconnect, (self.db_name))

    def test_connect_default(self):
        # Assert wheter connect() uses DEFAULT_DATABASE_NAME, even after
        # having connected and disconnected to a different db name
        connect('foo')
        disconnect('foo')
        conn = connect()
        self.assertEqual(conn.db, rethinkengine.connection.DEFAULT_DATABASE_NAME)
        disconnect()

    def test_disconnect_active_alias(self):
        # Assert whether disconnect() uses the active alias (and doesn't raise
        # a ConnectionError)
        connect('foo')
        disconnect()

    def test_disconnect_with_alias(self):
        # Assert whether disconnect() works when using an alias
        connect(self.db_name, alias='foo')
        disconnect('foo')
