"""Define internale migration V1."""
from yoyo.migrations import get_migration_hash


def upgrade(backend):
    """Apply v2 migration."""
    create_log_table(backend)
    create_version_table(backend)
    cursor = backend.execute("SELECT id, ctime FROM {}".format(backend.migration_table_quoted))
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
            "INSERT INTO TABLE {0.log_table_quoted} "
            "VALUES "
            "(:id, :migration_hash, :migration_id, 'apply', :created_at_utc, "
            ":username, :hostname, :comment)".format(backend),
            log_data,
        )
        backend.execute("COMMIT  {0.log_table_quoted} ".format(backend))

    create_migration_table(backend)
    cursor = backend.execute("SELECT count(*) FROM {0.log_table_quoted} ".format(backend))
    item = cursor.fetchone()
    if item:
        count = item[0]
        if count > 0:
            backend.execute(
                "INSERT INTO TABLE {0.migration_table_quoted} "
                "SELECT migration_hash, migration_id, created_at_utc "
                "FROM {0.log_table_quoted}".format(backend)
            )
            backend.execute("COMMIT  {0.migration_table_quoted} ".format(backend))


def create_migration_table(backend):
    backend.execute("drop table if exists {0.migration_table_quoted}".format(backend))
    backend.execute(
        "CREATE TABLE {0.migration_table_quoted} ( "
        # sha256 hash of the migration id
        "migration_hash STRING, "
        # The migration id (ie path basename without extension)
        "migration_id STRING, "
        # When this id was applied
        "applied_at_utc TIMESTAMP, "
        "INDEX (migration_hash))".format(backend)
    )


def create_log_table(backend):
    backend.execute("drop table if exists {0.log_table_quoted}".format(backend))
    backend.execute(
        "CREATE TABLE {0.log_table_quoted} ( "
        "id STRING, "
        "migration_hash STRING, "
        "migration_id STRING, "
        "operation STRING, "
        "username STRING, "
        "hostname STRING, "
        "comment STRING, "
        "created_at_utc TIMESTAMP, "
        "INDEX(id))".format(backend)
    )


def create_version_table(backend):
    backend.execute("drop table if exists {0.version_table_quoted}".format(backend))
    backend.execute(
        "CREATE TABLE {0.version_table_quoted} ("
        "version INT, "
        "installed_at_utc TIMESTAMP, INDEX(version))".format(backend)
    )
