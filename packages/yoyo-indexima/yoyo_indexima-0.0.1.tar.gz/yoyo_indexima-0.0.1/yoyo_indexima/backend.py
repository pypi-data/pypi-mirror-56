import time
from collections import Mapping
from datetime import datetime

from pyhive import hive
from yoyo import exceptions, get_backend as yoyo_get_backend, internalmigrations
from yoyo.backends import DatabaseBackend
from yoyo.connections import BACKENDS

from yoyo_indexima import v1, v2


__all__ = ['IndeximaBackend', 'register_indexima', 'get_backend']


epoch = datetime.utcfromtimestamp(0)


def dt_to_ms(dt):
    """Convert a datetime in unix timestamp."""
    delta = dt - epoch
    return int(delta.total_seconds() * 1000)


class IndeximaBackend(DatabaseBackend):
    """IndeximaBackend implementation.

    Stuff:
    - no driver module
    - add 'TABLE' after insert into ...
    - cast datetime to unix timestamp
    - remove transaction manager
    - add commit <<table name>> after each insert/delete...
    """

    driver_module = None

    log_table = 'yoyo_log'
    lock_table = 'yoyo_lock'
    version_table = 'yoyo_version'
    migration_table = 'yoyo_migration'

    mark_migration_sql = (
        "INSERT INTO TABLE {0.migration_table_quoted} " "VALUES (:migration_hash, :migration_id, :when)"
    )
    unmark_migration_sql = "DELETE FROM {0.migration_table_quoted} WHERE " "migration_hash = :migration_hash"
    applied_migrations_sql = (
        "SELECT migration_hash, applied_at_utc FROM " "{0.migration_table_quoted} " "ORDER by applied_at_utc"
    )
    create_test_table_sql = "CREATE TABLE {table_name_quoted} " "(id INT, INDEX(id))"
    log_migration_sql = (
        "INSERT INTO TABLE {0.log_table_quoted} "
        "VALUES (:id, :migration_hash, :migration_id, "
        ":operation, :username, :hostname, :created_at_utc)"
    )
    create_lock_table_sql = (
        "CREATE TABLE {0.lock_table_quoted} (" "locked INT, " "ctime TIMESTAMP," "pid INT," "INDEX (locked))"
    )

    list_tables_sql = "show tables "

    _driver = hive

    def connect(self, dburi):
        return hive.Connection(
            host=dburi.hostname if dburi.hostname else 'localhost',
            port=dburi.port if dburi.port else 10000,
            username=dburi.username if dburi.username else '',
            password=dburi.password if dburi.password else '',
            database=dburi.database if dburi.database else 'default',
            auth='CUSTOM',
        )

    def begin(self):
        """Indexima is always in a transaction, and has no "BEGIN" statement."""
        self._in_transaction = False

    def commit(self):
        self._in_transaction = False

    def rollback(self):
        self.init_connection(self.connection)
        self._in_transaction = False

    def _check_transactional_ddl(self):
        return False

    def quote_identifier(self, identifier):
        return f"{identifier}"

    def execute(self, sql, params=None):
        """Execute a query.

        Create a new cursor, execute a single statement and return the cursor
        object.

        :param sql: A single SQL statement, optionally with named parameters
                    (eg 'SELECT * FROM foo WHERE :bar IS NULL')
        :param params: A dictionary of parameters
        """
        if params and not isinstance(params, Mapping):
            raise TypeError("Expected dict or other mapping object")

        if params:
            # here we cast datetime object in timestamp
            for key in params:
                if isinstance(params[key], datetime):
                    params[key] = dt_to_ms(params[key])

        return super(IndeximaBackend, self).execute(sql=sql, params=params)

    def _insert_lock_row(self, pid, timeout, poll_interval=0.5):
        poll_interval = min(poll_interval, timeout)
        started = time.time()
        while True:
            try:
                with self.transaction():
                    self.execute(
                        "INSERT INTO TABLE {} " "VALUES (1, :when, :pid)".format(self.lock_table_quoted),
                        {'when': datetime.utcnow(), 'pid': pid},
                    )
                    self.execute("COMMIT {}".format(self.lock_table_quoted))
            except self.DatabaseError:
                if timeout and time.time() > started + timeout:
                    cursor = self.execute("SELECT pid FROM {}".format(self.lock_table_quoted))
                    row = cursor.fetchone()
                    if row:
                        raise exceptions.LockTimeout(
                            "Process {} has locked this database "
                            "(run yoyo break-lock to remove this lock)".format(row[0])
                        )
                    else:
                        raise exceptions.LockTimeout(
                            "Database locked " "(run yoyo break-lock to remove this lock)"
                        )
                time.sleep(poll_interval)
            else:
                return

    def unmark_one(self, migration, log=True):
        self.ensure_internal_schema_updated()
        sql = self.unmark_migration_sql.format(self)
        self.execute(sql, {'migration_hash': migration.hash})
        self.execute("COMMIT {}".format(self.migration_table_quoted))
        if log:
            self.log_migration(migration, 'unmark')

    def log_migration(self, migration, operation, comment=None):
        super(IndeximaBackend, self).log_migration(migration=migration, operation=operation, comment=comment)
        self.execute("COMMIT {}".format(self.log_table_quoted))

    def _delete_lock_row(self, pid):
        super(IndeximaBackend, self)._delete_lock_row(pid=pid)
        self.execute("COMMIT {}".format(self.lock_table_quoted))

    def break_lock(self):
        super(IndeximaBackend, self).break_lock()
        self.execute("COMMIT {}".format(self.lock_table_quoted))


def _get_current_version(backend):
    """Return the currently installed yoyo migrations schema version."""
    tables = set(backend.list_tables())
    version_table = backend.version_table
    if backend.migration_table not in tables:
        return 0
    if version_table not in tables:
        return 1
    with backend.transaction():
        cursor = backend.execute(
            "SELECT max(version) FROM {} ".format(backend.quote_identifier(version_table))
        )
        item = cursor.fetchone()
        if item:
            version = item[0]
            assert version in internalmigrations.schema_versions
            return version
        return 0


def _mark_schema_version(backend, version):
    """Mark schema version in version table."""
    assert version in internalmigrations.schema_versions
    if version < internalmigrations.USE_VERSION_TABLE_FROM:
        return
    backend.execute(
        "INSERT INTO TABLE {0.version_table_quoted} VALUES (:version, :when)".format(backend),
        {'version': version, 'when': datetime.utcnow()},
    )
    backend.execute("COMMIT {0.version_table_quoted}".format(backend))


def register_indexima():
    """Register all our stuff."""
    # register indexima backend
    BACKENDS['indexima'] = IndeximaBackend

    # override migration schema migration implementation
    internalmigrations.schema_versions = {0: None, 1: v1, 2: v2}
    # override migration function
    internalmigrations.mark_schema_version = _mark_schema_version
    internalmigrations.get_current_version = _get_current_version


def get_backend(uri):
    """Return associated backend."""
    register_indexima()
    return yoyo_get_backend(uri=uri, migration_table=IndeximaBackend.migration_table)
