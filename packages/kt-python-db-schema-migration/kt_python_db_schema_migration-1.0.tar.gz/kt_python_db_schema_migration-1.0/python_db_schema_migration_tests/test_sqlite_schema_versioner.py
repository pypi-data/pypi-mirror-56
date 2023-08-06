from python_db_schema_migration import SqliteSchemaVersioner
from .base_sqlite_test_case import BaseSqliteTestCase


class TestSqliteSchemaVersioner(BaseSqliteTestCase):
    def test_no_schema_version(self):
        versioner = SqliteSchemaVersioner(self.sqlite_file)
        assert versioner.get_schema_version() == 0

    def test_set_schema_version(self):
        versioner = SqliteSchemaVersioner(self.sqlite_file)
        versioner.set_schema_version(1)
        assert versioner.get_schema_version() == 1
