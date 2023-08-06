"""Indexima Backend implementation."""
import time
from collections import Mapping
from datetime import datetime
from typing import Optional

from pyhive import hive
from yoyo import exceptions
from yoyo.backends import DatabaseBackend
from yoyo.connections import DatabaseURI

from yoyo_indexima.internalmigrations import needs_upgrading, upgrade


__all__ = ['IndeximaBackend']


class IndeximaBackend(DatabaseBackend):
    """IndeximaBackend implementation.

    Stuff:
    - no driver module
    - add 'TABLE' after insert into ...
    - cast datetime to indexima timestamp
    - remove transaction manager
    - add commit <<table name>> after each insert/delete...
    - add typing
    - integrate yoyo internal migration
    """

    driver_module = None

    log_table: str = 'yoyo_log'
    lock_table: str = 'yoyo_lock'
    version_table: str = 'yoyo_version'
    migration_table: str = 'yoyo_migration'

    mark_migration_sql: str = (
        "INSERT INTO TABLE {0.migration_table_quoted} VALUES (:migration_hash, :migration_id, :when)"
    )
    unmark_migration_sql: str = (
        "DELETE FROM {0.migration_table_quoted} WHERE  migration_hash = :migration_hash"
    )
    applied_migrations_sql: str = (
        "SELECT migration_hash, applied_at_utc FROM {0.migration_table_quoted} ORDER by applied_at_utc"
    )
    create_test_table_sql: str = "CREATE TABLE {table_name_quoted} (id INT, INDEX(id))"
    log_migration_sql: str = (
        "INSERT INTO TABLE {0.log_table_quoted} "
        "VALUES (:id, :migration_hash, :migration_id, "
        ":operation, :username, :hostname, :created_at_utc)"
    )
    create_lock_table_sql: str = (
        "CREATE TABLE {0.lock_table_quoted} ("
        "locked INT, "
        "ctime TIMESTAMP(SECOND),"
        "pid INT,"
        "INDEX (locked))"
    )

    list_tables_sql: str = "show tables "

    _driver = hive

    def connect(
        self,
        dburi: DatabaseURI,
        default_auth: Optional[str] = 'CUSTOM',
        default_database: Optional[str] = 'default',
        default_port: Optional[int] = 10000,
    ) -> hive.Connection:

        _auth = dburi.args['auth'] if "auth" in dburi.args else default_auth
        _database = dburi.database if dburi.database else default_database

        return hive.Connection(
            host=dburi.hostname if dburi.hostname else 'localhost',
            port=dburi.port if dburi.port else default_port,
            username=dburi.username if dburi.username else None,  # TODO: check default value
            password=dburi.password if dburi.password else None,  # TODO: check default value
            database=_database,
            auth=_auth,
        )

    def begin(self):
        """Indexima is always in a transaction, and has no "BEGIN" statement."""
        self._in_transaction = False

    def commit(self):
        """With indexima we need to commit/rollback a table (with her name)."""
        self._in_transaction = False

    def rollback(self):
        """With indexima we need to commit/rollback a table (with her name)."""
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
            # here we format datetime object in indexima timestamp...
            # source: https://indexima.com/support/doc/v.1.6/Handling_Data_Spaces/Data_Types.html
            # format yyyy-mm-dd hh:mm:ss
            for key in params:
                if isinstance(params[key], datetime):
                    _dt = params[key]
                    params[key] = _dt.strftime('%Y-%m-%d %H:%M:%S')

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
                    self.execute(f"COMMIT {self.lock_table_quoted}")
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

    def unmark_one(self, migration, log: Optional[bool] = True):
        self.ensure_internal_schema_updated()
        sql = self.unmark_migration_sql.format(self)
        self.execute(sql, {'migration_hash': migration.hash})
        self.execute(f"COMMIT {self.migration_table_quoted}")
        if log:
            self.log_migration(migration, 'unmark')

    def log_migration(self, migration, operation, comment=None):
        super(IndeximaBackend, self).log_migration(migration=migration, operation=operation, comment=comment)
        self.execute(f"COMMIT {self.log_table_quoted}")

    def _delete_lock_row(self, pid):
        super(IndeximaBackend, self)._delete_lock_row(pid=pid)
        self.execute(f"COMMIT {self.lock_table_quoted}")

    def break_lock(self):
        super(IndeximaBackend, self).break_lock()
        self.execute(f"COMMIT {self.lock_table_quoted}")

    def ensure_internal_schema_updated(self):
        """Check and upgrade yoyo's internal schema."""
        if self._internal_schema_updated:
            return
        if needs_upgrading(self):
            assert not self._in_transaction
            with self.lock():
                upgrade(self)
                self.connection.commit()
                self._internal_schema_updated = True
