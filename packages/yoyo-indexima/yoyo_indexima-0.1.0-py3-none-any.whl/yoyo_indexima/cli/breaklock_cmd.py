from yoyo_indexima.cli.common import get_backend_from_args, print_command


__all__ = ['create_break_lock_parser', 'break_lock']


def create_break_lock_parser(global_parser, subparsers):
    """Create Break lock parser."""
    parser_break_lock = subparsers.add_parser(
        'break-lock', parents=[global_parser], help="Break migration locks"
    )
    parser_break_lock.set_defaults(func=break_lock, command_name='break-lock')
    parser_break_lock.add_argument('-u', '--uri', type=str, help='backend uri', default=None, required=True)


def break_lock(args):
    print_command(message='Break lock')
    backend = get_backend_from_args(args=args)
    backend.break_lock()
