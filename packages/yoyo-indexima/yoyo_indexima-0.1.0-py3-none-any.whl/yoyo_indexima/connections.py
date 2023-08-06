"""Connections utility.

Change:

- get_backend use migration table name from Backend class
- register indexima backend on first call
- add typing

"""
from yoyo import get_backend as yoyo_get_backend
from yoyo.backends import DatabaseBackend
from yoyo.connections import BACKENDS

from .backend import IndeximaBackend


__all__ = ['get_backend']


def register_indexima():
    """Register all our stuff."""

    # don't resgister twice
    if IndeximaBackend in BACKENDS:
        return

    # register indexima backend
    BACKENDS['indexima'] = IndeximaBackend


def get_backend(uri: str) -> DatabaseBackend:
    """Return associated backend."""
    register_indexima()
    return yoyo_get_backend(uri=uri, migration_table=IndeximaBackend.migration_table)
