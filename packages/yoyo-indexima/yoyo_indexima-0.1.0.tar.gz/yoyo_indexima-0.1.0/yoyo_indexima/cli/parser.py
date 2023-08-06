"""Define parser."""
import argparse

from yoyo_indexima.cli import breaklock_cmd, migration_cmd


__all__ = ['create_parser']


def create_parser():
    """Create main parser."""
    global_parser = argparse.ArgumentParser(add_help=False)
    argparser = argparse.ArgumentParser(prog='yoyo_indexima', parents=[global_parser])
    subparsers = argparser.add_subparsers(help='Commands help')

    migration_cmd.create_migration_parser(global_parser=global_parser, subparsers=subparsers)
    breaklock_cmd.create_break_lock_parser(global_parser=global_parser, subparsers=subparsers)

    return argparser
