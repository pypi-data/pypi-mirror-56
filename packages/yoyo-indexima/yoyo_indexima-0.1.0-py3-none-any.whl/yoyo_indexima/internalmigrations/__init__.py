"""Migrate yoyo's internal table structure.

Changes:

  - use function in SCHEMA_VERSIONS rather than module reference
  - add typing
  - add docstyle
  - manage error case with no data in version table (indexima v 1.6)
  - add indexima commit command
"""

from datetime import datetime
from typing import Callable, Dict, Optional

from yoyo.backends import DatabaseBackend

from .v1 import upgrade as upgrade_v1
from .v2 import upgrade as update_v2


#: Mapping of {schema version number: module}
SCHEMA_VERSIONS: Dict[str, Callable[[DatabaseBackend], None]] = {0: None, 1: upgrade_v1, 2: update_v2}


#: First schema version that supports the yoyo_versions table
USE_VERSION_TABLE_FROM = 2


__all__ = ['needs_upgrading', 'upgrade', 'get_current_version', 'mark_schema_version']


def needs_upgrading(backend: DatabaseBackend) -> bool:
    """Check the currently installed yoyo migrations version.

    # Parameters
        backend (DatabaseBackend): backend instance

    # Returns
        (bool): True if the backend needs to be upraded
    """
    return get_current_version(backend) < max(SCHEMA_VERSIONS)


def upgrade(backend: DatabaseBackend, version: Optional[int] = None):
    """Check the currently installed yoyo migrations version and update the internal schema.

    # Parameters
        backend (DatabaseBackend): backend instance to upgrade
        version (Optional[int]): desired version (default is last version)

    """

    if version is None:
        desired_version = max(SCHEMA_VERSIONS)
    else:
        desired_version = version
    current_version = get_current_version(backend)
    with backend.transaction():
        while current_version < desired_version:
            next_version = current_version + 1
            SCHEMA_VERSIONS[next_version].upgrade(backend)
            current_version = next_version
            mark_schema_version(backend, current_version)


def get_current_version(backend: DatabaseBackend) -> int:
    """Return the currently installed yoyo migrations schema version.

    # Parameters
        backend (DatabaseBackend): backend instance

    # Returns
        (int): the current schema version
    """
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
        # Here we manage the case when no previous version was found.
        # Could occurs when things goes wrong
        if item:
            version = item[0]
            assert version in SCHEMA_VERSIONS
            return version
        return 0


def mark_schema_version(backend: DatabaseBackend, version: int):
    """Mark the given version as having been applied.

    # Parameters
        backend (DatabaseBackend): backend instance
        version (int): current version
    """
    assert version in SCHEMA_VERSIONS
    if version < USE_VERSION_TABLE_FROM:
        return
    backend.execute(
        "INSERT INTO TABLE {0.version_table_quoted} VALUES (:version, :when)".format(backend),
        {'version': version, 'when': datetime.utcnow()},
    )
    backend.execute("COMMIT {0.version_table_quoted}".format(backend))
