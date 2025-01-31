import sqlite3
from src.utils.database_utils import init_db
from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestDatabaseUtils(TestCase):

    @patch('sqlite3.connect')
    def test_init_db_calls_connect(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        init_db()

        mock_connect.assert_called_once_with('heatmap_app.db')
        mock_conn.close.assert_called_once()

    @patch('sqlite3.connect')
    def test_init_db_users_table_creation(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        init_db()

        mock_cursor.execute.assert_any_call('''
            CREATE TABLE IF NOT EXISTS users
            (username TEXT PRIMARY KEY, 
             password_hash TEXT,
             created_at DATETIME)
        ''')

    @patch('sqlite3.connect')
    def test_init_db_station_ratings_table_creation(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        init_db()

        mock_cursor.execute.assert_any_call('''
            CREATE TABLE IF NOT EXISTS station_ratings
            (station_id TEXT,
             username TEXT,
             rating INTEGER,
             timestamp DATETIME,
             FOREIGN KEY(username) REFERENCES users(username))
        ''')

    @patch('sqlite3.connect')
    def test_init_db_commits_changes(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        init_db()

        mock_conn.commit.assert_called_once()



