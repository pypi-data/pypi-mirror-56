import sqlite3
from .sqlite_execute import sqlite_execute
from .schema_versioner import SchemaVersioner


class SqliteSchemaVersioner(SchemaVersioner):
    def __init__(self, sqlite_file: str):
        self.sqlite_file = sqlite_file
        if not self._have_schema_version():
            for statement in [
                'CREATE TABLE schema_version (v INTEGER)',
                'INSERT INTO schema_version (v) VALUES(0)',
            ]:
                with sqlite_execute(self._new_conn(), statement):
                    pass

    def _new_conn(self):
        return sqlite3.connect(self.sqlite_file)

    def _have_schema_version(self) -> bool:
        with sqlite_execute(self._new_conn(), 'PRAGMA table_info(schema_version)') as cursor:
            results = cursor.fetchall()
            return len(results) != 0

    def get_schema_version(self) -> int:
        with sqlite_execute(self._new_conn(), 'SELECT v FROM schema_version') as cursor:
            result = cursor.fetchone()
            return result[0]

    def set_schema_version(self, v: int):
        with sqlite_execute(self._new_conn(), 'UPDATE schema_version SET v = ?', (v,)):
            pass
