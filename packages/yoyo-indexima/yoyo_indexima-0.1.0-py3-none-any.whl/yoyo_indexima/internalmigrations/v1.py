"""Version 1 schema.

Compatible with yoyo-migrations < 6.0

Change:

  - refactor upgrade function
  - Indexima timestamp format
  - add typing

"""
from yoyo.backends import DatabaseBackend


__all__ = ['upgrade']


def upgrade(backend: DatabaseBackend):
    """Apply V1 migration."""
    backend.execute(f"drop table if exists {backend.migration_table_quoted}")
    _create_migration_table(backend=backend)


def _create_migration_table(backend: DatabaseBackend):
    backend.execute(
        f"CREATE TABLE {backend.migration_table_quoted} (" "id STRING," "ctime TIMESTAMP(SECOND), INDEX(id))"
    )
