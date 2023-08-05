"""Define internale migration V1."""


def upgrade(backend):
    """Apply V1 migration."""
    backend.execute("drop table if exists {0.migration_table_quoted}".format(backend))
    backend.execute(
        "CREATE TABLE {0.migration_table_quoted} (" "id STRING," "ctime TIMESTAMP, INDEX(id))".format(backend)
    )
