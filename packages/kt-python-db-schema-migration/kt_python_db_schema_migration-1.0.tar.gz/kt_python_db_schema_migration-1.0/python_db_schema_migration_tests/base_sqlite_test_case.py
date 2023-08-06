import unittest
import os


class BaseSqliteTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sqlite_file = 'test_sqlite.db'
        self._delete_sqlite()

    def tearDown(self) -> None:
        self._delete_sqlite()

    def _delete_sqlite(self):
        if os.path.exists(self.sqlite_file):
            os.remove(self.sqlite_file)
