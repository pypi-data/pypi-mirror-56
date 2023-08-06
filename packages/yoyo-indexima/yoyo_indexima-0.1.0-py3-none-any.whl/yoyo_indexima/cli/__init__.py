"""Define python client command."""
import logging

from yoyo_indexima.cli.common import InvalidArgument
from yoyo_indexima.cli.parser import create_parser
from yoyo_indexima.logger import init_root_logger


logger = logging.getLogger('yoyo_indexima.cli')

__all__ = ['main']


def main():

    argparser = create_parser()

    args = argparser.parse_args()

    init_root_logger()

    if 'func' not in args:
        print('Please specify a command or -h for help')
        return -1

    try:
        args.func(args)
    except InvalidArgument as e:
        argparser.error(e.args[0])

    return 0
