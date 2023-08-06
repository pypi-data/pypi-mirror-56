# Copyright 2015 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import logging
import os

from yoyo import ancestors, descendants, read_migrations
from yoyo.backends import DatabaseBackend
from yoyo.migrations import MigrationList

from yoyo_indexima.cli.common import InvalidArgument, get_backend_from_args, print_command


logger = logging.getLogger('yoyo_indexima.cli')


__all__ = ['create_migration_parser', 'show', 'apply', 'reapply', 'rollback', 'mark', 'unmark']


def create_migration_parser(global_parser, subparsers):
    """Create migration parser."""
    migration_parser = argparse.ArgumentParser(description='Indexima migration tool', add_help=False)
    migration_parser.add_argument(
        '-s',
        '--source',
        type=str,
        help='source path of migration script (default ./migrations)',
        required=False,
    )
    migration_parser.add_argument('-u', '--uri', type=str, help='backend uri', default=None, required=True)
    migration_parser.add_argument(
        '-f',
        '--force',
        default=False,
        action="store_true",
        help='Force apply/rollback of steps even if previous steps have failed',
        required=False,
    )
    migration_parser.add_argument(
        '-a',
        '--all',
        dest="all",
        default=False,
        action="store_true",
        help="Select all migrations, regardless of whether they have been previously applied",
        required=False,
    )
    migration_parser.add_argument(
        '-r', '--revision', help="Apply/rollback migration with id REVISION", metavar='REVISION'
    )
    migration_parser.add_argument(
        '-d',
        '--dry-run',
        dest="dry_run",
        default=False,
        action="store_true",
        help="Dry run: no modification will be applied",
        required=False,
    )
    parser_show = subparsers.add_parser(
        'show', help="Show migrations", parents=[global_parser, migration_parser]
    )
    parser_show.set_defaults(func=show, command_name='show')

    parser_apply = subparsers.add_parser(
        'apply', help="Apply migrations", parents=[global_parser, migration_parser]
    )
    parser_apply.set_defaults(func=apply, command_name='apply')

    parser_reapply = subparsers.add_parser(
        'reapply', parents=[global_parser, migration_parser], help="Reapply migrations"
    )
    parser_reapply.set_defaults(func=reapply, command_name='reapply')

    parser_rollback = subparsers.add_parser(
        'rollback', parents=[global_parser, migration_parser], help="Rollback migrations"
    )
    parser_rollback.set_defaults(func=rollback, command_name='rollback')

    parser_mark = subparsers.add_parser(
        'mark',
        parents=[global_parser, migration_parser],
        help="Mark migrations as applied, without running them",
    )
    parser_mark.set_defaults(func=mark, command_name='mark')

    parser_unmark = subparsers.add_parser(
        'unmark',
        parents=[global_parser, migration_parser],
        help="Unmark applied migrations, without rolling them back",
    )
    parser_unmark.set_defaults(func=unmark, command_name='unmark')


def get_migrations(args, backend: DatabaseBackend) -> MigrationList:
    """Return selected migration according command."""
    source = args.source if args.source else os.path.join(os.getcwd(), 'migrations')
    migrations: MigrationList = read_migrations(source)

    if not args.all:
        if args.func in {apply, show, mark}:
            migrations = backend.to_apply(migrations)
        elif args.func in {rollback, reapply, unmark}:
            migrations = backend.to_rollback(migrations)

    if args.revision:
        targets = [m for m in migrations if args.revision in m.id]
        if len(targets) == 0:
            raise InvalidArgument(f"'{args.revision}' doesn't match any revisions.")
        if len(targets) > 1:
            raise InvalidArgument(
                "'{}' matches multiple revisions. "
                "Please specify one of {}.".format(args.revision, ', '.join(m.id for m in targets))
            )

        target = targets[0]

        # apply: apply target an all its dependencies
        if args.func in {mark, apply}:
            deps = ancestors(target, migrations)
            target_plus_deps = deps | {target}
            migrations = migrations.filter(lambda m: m in target_plus_deps)

        # rollback/reapply: rollback target and everything that depends on it
        else:
            deps = descendants(target, migrations)
            target_plus_deps = deps | {target}
            migrations = migrations.filter(lambda m: m in target_plus_deps)

    return migrations


def show(args):
    print_command(message='Pending Migrations')
    backend = get_backend_from_args(args=args)
    with backend.lock():
        migrations = get_migrations(args=args, backend=backend)
        for _migration in migrations:
            logger.info(_migration)
        print_command(message=f"{len(migrations)} pending migrations found")


def apply(args):
    print_command(message=f'Apply Migrations')
    backend = get_backend_from_args(args=args)
    with backend.lock():
        migrations = get_migrations(args=args, backend=backend)
        if not args.dry_run:
            backend.apply_migrations(migrations=migrations, force=args.force)
        print_command(message=f"{len(migrations)} migrations applied")


def reapply(args):
    print_command(message='ReApply Migrations')
    backend = get_backend_from_args(args=args)
    with backend.lock():
        migrations = get_migrations(args, backend)
        print_command(message=f"{len(migrations)} migrations to rollback")
        if not args.dry_run:
            backend.rollback_migrations(migrations, args.force)
            migrations = backend.to_apply(migrations)
            backend.apply_migrations(migrations, args.force)
            print_command(message=f"{len(migrations)} migrations applied")


def rollback(args):
    print_command(message='Rollback Migrations')
    backend = get_backend_from_args(args=args)
    with backend.lock():
        migrations = get_migrations(args, backend)
        if not args.dry_run:
            backend.rollback_migrations(migrations, args.force)
        print_command(message=f"{len(migrations)} migrations rollbacked")


def mark(args):
    print_command(message='Mark Migrations')
    backend = get_backend_from_args(args=args)
    with backend.lock():
        migrations = get_migrations(args, backend)
        if not args.dry_run:
            backend.mark_migrations(migrations)
        print_command(message=f"{len(migrations)} migrations marked")


def unmark(args):
    print_command(message='Unmark Migrations')
    backend = get_backend_from_args(args=args)
    with backend.lock():
        migrations = get_migrations(args, backend)
        if not args.dry_run:
            backend.unmark_migrations(migrations)
        print_command(message=f"{len(migrations)} migrations unmarked")
