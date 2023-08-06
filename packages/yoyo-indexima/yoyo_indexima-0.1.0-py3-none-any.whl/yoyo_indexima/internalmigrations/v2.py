"""
Version 2 schema.

Compatible with yoyo-migrations >=  6.0

Change:

  - Indexima COMMIT
  - refactor upgrade function
  - manage case with no previous migration
  - Indexima timestamp format
"""
from yoyo.backends import DatabaseBackend
from yoyo.migrations import get_migration_hash


__all__ = ['upgrade']


def upgrade(backend: DatabaseBackend):
    """Apply v2 migration."""
    _create_log_table(backend=backend)
    _create_version_table(backend=backend)

    # upgrate migration table
    _migrate_v1_to_log_table(backend=backend)
    _drop_old_migration_table(backend=backend)
    _create_migration_table(backend=backend)
    _migrate_log_to_v2_table(backend=backend)


def _migrate_log_to_v2_table(backend: DatabaseBackend):
    """Insert log table into migration."""
    cursor = backend.execute(f"SELECT count(*) FROM {backend.log_table_quoted} ")
    item = cursor.fetchone()
    if item:
        count = item[0]
        if count > 0:
            backend.execute(
                f"INSERT INTO TABLE {backend.migration_table_quoted} "
                "SELECT migration_hash, migration_id, created_at_utc "
                f"FROM {backend.log_table_quoted}"
            )
            backend.execute(f"COMMIT  {backend.migration_table_quoted} ")


def _migrate_v1_to_log_table(backend: DatabaseBackend):
    """Insert migration v1 data into log table."""
    cursor = backend.execute(f"SELECT id, ctime FROM {backend.migration_table_quoted}")
    for migration_id, created_at in iter(cursor.fetchone, None):
        migration_hash = get_migration_hash(migration_id)
        log_data = dict(
            backend.get_log_data(),
            operation='apply',
            comment=('this log entry created automatically by an ' 'internal schema upgrade'),
            created_at_utc=created_at,
            migration_hash=migration_hash,
            migration_id=migration_id,
        )
        backend.execute(
            f"INSERT INTO TABLE {backend.log_table_quoted} "
            "VALUES "
            "(:id, :migration_hash, :migration_id, 'apply', :created_at_utc, "
            ":username, :hostname, :comment)",
            log_data,
        )
        backend.execute(f"COMMIT  {backend.log_table_quoted} ")


def _drop_old_migration_table(backend: DatabaseBackend):
    backend.execute(f"drop table if exists {backend.migration_table_quoted}")


def _create_migration_table(backend: DatabaseBackend):
    backend.execute(
        f"CREATE TABLE {backend.migration_table_quoted} ( "
        # sha256 hash of the migration id
        "migration_hash STRING, "
        # The migration id (ie path basename without extension)
        "migration_id STRING, "
        # When this id was applied
        "applied_at_utc TIMESTAMP(SECOND), "
        "INDEX (migration_hash))"
    )


def _create_log_table(backend: DatabaseBackend):
    # backend.execute(f"drop table if exists {backend.log_table_quoted}")
    backend.execute(
        f"CREATE TABLE IF NOT EXISTS {backend.log_table_quoted} ( "
        "id STRING, "
        "migration_hash STRING, "
        "migration_id STRING, "
        "operation STRING, "
        "username STRING, "
        "hostname STRING, "
        "comment STRING, "
        "created_at_utc TIMESTAMP(SECOND), "
        "INDEX(id))"
    )


def _create_version_table(backend: DatabaseBackend):
    # backend.execute(f"drop table if exists {backend.version_table_quoted}")
    backend.execute(
        f"CREATE TABLE IF NOT EXISTS {backend.version_table_quoted} ("
        "version INT, "
        "installed_at_utc TIMESTAMP(SECOND), INDEX(version))"
    )
