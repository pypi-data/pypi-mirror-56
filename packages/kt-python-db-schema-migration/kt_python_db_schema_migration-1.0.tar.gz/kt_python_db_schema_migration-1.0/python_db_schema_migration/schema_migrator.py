import logging
from typing import List, Dict
from .migration import Migration
from .schema_versioner import SchemaVersioner


class SchemaMigrator(object):
    def __init__(self, schema_versioner: SchemaVersioner, migrations: List[Migration]):
        self.logger = logging.getLogger('kt_python_db_schema_migration')
        self.logger.setLevel(logging.INFO)
        self.schema_versioner = schema_versioner
        if not migrations:
            raise RuntimeError("Need to have at least one migration")
        self.latest_schema_version = max(map(lambda m: m.to_version(), migrations))
        # check if all migrations form a linear sequence
        # e.g. migrations can be ordered (0...latest_schema_version - 1) w.r.t. from_version
        if set(map(lambda m: m.from_version(), migrations)) != set([i for i in range(0, self.latest_schema_version)]):
            raise RuntimeError(f'Migrations are not linear. '
                               f'Expected latest schema version is {self.latest_schema_version}')
        self.migrations = {}  # type: Dict[int, Migration]
        for migration in migrations:
            self.migrations[migration.from_version()] = migration

    def migrate(self):
        current_schema_version = self.schema_versioner.get_schema_version()
        if current_schema_version == self.latest_schema_version:
            self.logger.info(f"Already on latest schema version {self.latest_schema_version}")
            return
        migrate_from_versions = [i for i in range(current_schema_version, self.latest_schema_version)]
        for migrate_from_version in migrate_from_versions:
            self.logger.info(f"Executing schema migration from version {migrate_from_version}")
            migration = self.migrations[migrate_from_version]
            migration.execute()
            self.schema_versioner.set_schema_version(migration.to_version())
