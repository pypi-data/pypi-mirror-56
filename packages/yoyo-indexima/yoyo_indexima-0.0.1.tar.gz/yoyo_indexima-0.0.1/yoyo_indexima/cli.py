"""Define python client."""
import argparse
import logging
import os

from yoyo import get_backend, read_migrations

from yoyo_indexima.backend import IndeximaBackend, register_indexima
from yoyo_indexima.logger import init_root_logger


logger = logging.getLogger('yoyo_indexima.cli')


def show_migration(backend, migrations):
    logger.info(f"{'-'*80}")
    logger.info('Pending Migrations')
    for _migration in backend.to_apply(migrations):
        logger.info(_migration)
    logger.info(f"{'-'*80}")


def apply_migration(backend, migrations):
    logger.info(f"{'-'*80}")
    logger.info('Applying Migrations')
    with backend.lock():
        _to_apply = backend.to_apply(migrations)
        logger.info(f'{len(_to_apply)} pending Migrations')
        backend.apply_migrations(_to_apply)
    logger.info(f"{'-'*80}")


def main():
    parser = argparse.ArgumentParser(description='Indexima migration tool')
    parser.add_argument('command', type=str, help='command (show, apply)', choices=['show', 'apply'])
    parser.add_argument(
        '-s',
        '--source',
        type=str,
        help='source path of migration script (default ./migrations)',
        required=False,
    )
    parser.add_argument('-u', '--uri', type=str, help='backend uri', required=True)

    args = parser.parse_args()

    init_root_logger()
    register_indexima()

    backend = get_backend(uri=args.uri, migration_table=IndeximaBackend.migration_table)

    source = args.source if args.source else os.path.join(os.getcwd(), 'migrations')

    migrations = read_migrations(source)
    if not len(migrations):
        logger.info('no migrations found')
        return 0

    if args.command == 'show':
        show_migration(backend=backend, migrations=migrations)
    elif args.command == 'apply':
        apply_migration(backend=backend, migrations=migrations)

    return 0
