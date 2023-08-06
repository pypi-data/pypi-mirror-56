import argparse
import sys

from conapp.commands import config, snapshots, local
from conapp import VERSION

COMMANDS = [
    config,
    snapshots,
    local
]


def get_args(args: list) -> argparse.Namespace:
    """Build an argparser and return a Namespace"""

    parser = argparse.ArgumentParser(prog='conapp', description='conapp a simple Config Applier')

    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version info"
    )

    sub_parser = parser.add_subparsers(
        title="Commands",
        description="Valid commands",
        help="sub-command help",
    )

    for command in COMMANDS:
        command.setup_arguments(
            sub_parser.add_parser(
                command.COMMAND,
                help=command.COMMAND_HELP
            )
        )

    def default(args: argparse.Namespace) -> None:
        if args.version:
            print(VERSION)
            exit(0)

        parser.print_usage()
        sys.exit(1)

    # TODO: Add other commands
    parser.set_defaults(command=default)

    return parser.parse_args(args=args)
