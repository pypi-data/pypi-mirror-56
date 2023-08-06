import sqlite3
from python_db_schema_migration import SqliteSchemaVersioner, SchemaMigrator, Migration
from python_db_schema_migration.sqlite_execute import sqlite_execute
from .base_sqlite_test_case import BaseSqliteTestCase


class AddJobsTable(Migration):
    def __init__(self, sqlite_file: str):
        self.sqlite_file = sqlite_file  # type: str

    def from_version(self) -> int:
        return 0

    def execute(self):
        with sqlite_execute(
                sqlite3.connect(self.sqlite_file),
                'CREATE TABLE jobs (title TEXT)'
        ):
            pass


class AddSalaryColumnToJobsTable(Migration):
    def __init__(self, sqlite_file: str):
        self.sqlite_file = sqlite_file  # type: str

    def from_version(self) -> int:
        return 1

    def execute(self):
        with sqlite_execute(
                sqlite3.connect(self.sqlite_file),
                'ALTER TABLE jobs ADD salary INT'
        ):
            pass


class DummyNonLinearMigration(Migration):
    def from_version(self) -> int:
        return 3

    def execute(self):
        pass


class TestSchemaMigratorWithSqlite(BaseSqliteTestCase):
    def test_one_migration(self):
        versioner = SqliteSchemaVersioner(self.sqlite_file)
        migrator = SchemaMigrator(versioner, [AddJobsTable(self.sqlite_file)])
        migrator.migrate()
        with sqlite_execute(
                sqlite3.connect(self.sqlite_file),
                'INSERT INTO jobs VALUES (?)',
                ('Software Engineer',)
        ):
            pass

    def test_two_migrations(self):
        versioner = SqliteSchemaVersioner(self.sqlite_file)
        migrator = SchemaMigrator(versioner, [
            # out of order should also be fine
            AddSalaryColumnToJobsTable(self.sqlite_file),
            AddJobsTable(self.sqlite_file),
        ])
        migrator.migrate()
        with sqlite_execute(
                sqlite3.connect(self.sqlite_file),
                'INSERT INTO jobs VALUES (?, ?)',
                ('Software Engineer', 200000)
        ):
            pass

    def test_idempotent_migrations(self):
        versioner = SqliteSchemaVersioner(self.sqlite_file)
        migrator = SchemaMigrator(versioner, [
            # out of order should also be fine
            AddSalaryColumnToJobsTable(self.sqlite_file),
            AddJobsTable(self.sqlite_file),
        ])
        for _ in range(10):
            migrator.migrate()

    def test_throw_at_non_linear_migrations(self):
        exception_thrown = False
        versioner = SqliteSchemaVersioner(self.sqlite_file)
        try:
            SchemaMigrator(versioner, [
                AddJobsTable(self.sqlite_file),
                AddSalaryColumnToJobsTable(self.sqlite_file),
                DummyNonLinearMigration()
            ])
        except RuntimeError:
            exception_thrown = True
        finally:
            assert exception_thrown
