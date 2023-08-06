"""Define utilities."""
import logging

from yoyo.backends import DatabaseBackend

from yoyo_indexima.connections import get_backend


__all__ = ['InvalidArgument', 'get_backend_from_args', 'print_command']

logger = logging.getLogger('yoyo_indexima.cli')


class InvalidArgument(Exception):
    pass


def get_backend_from_args(args) -> DatabaseBackend:
    return get_backend(uri=args.uri)


def print_command(message: str):
    logger.info(
        f"""
    {'-'*80}
    {message}
    {'-'*80}
    """
    )
