import os
import argparse
import sys

from conapp.file_paths import get_config_dir, CONFIG_SNAPSHOT_DIR, get_snapshot_by_rel
from conapp.file_ops import create_snapshot, apply_snapshot

COMMAND = 'snapshots'
COMMAND_HELP = "manage snapshots"

def setup_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Setup arguments for snapshots command
    """

    parser.set_defaults(command=main)

    subparsers = parser.add_subparsers(
        title=f"{COMMAND} commands",
        description="commands for managing snapshots"
    )

    list_parser = subparsers.add_parser('list', help="list available snapshots (default)")

    delete_parser = subparsers.add_parser('delete', help="remove snapshots")
    # TODO: Flush this out
    delete_parser.set_defaults(command=delete_snapshot)
    delete_parser.add_argument(
        'snapshot',
        help="snapshot to delete",
        type=int
    )
    delete_parser.add_argument(
        '--dry-run',
        action="store_true",
        help="don't delete the file"
    )

    apply_parser = subparsers.add_parser('apply', help="apply a snapshot, defaults to newest")
    apply_parser.set_defaults(command=restore_snapshot)
    apply_parser.add_argument(
        'snapshot',
        default=0,
        help="The snapshot to apply, defaults to 0",
        nargs="?",
        type=int
    )
    apply_parser.add_argument(
        '--no-backup',
        action='store_true',
        help="Don't create a snapshot before restoring. Use at own risk!"
    )
    apply_parser.add_argument(
        '--no-apply',
        action='store_true',
        help="Don't apply snapshot, will still create a backup"
    )

    return parser


def main(args: argparse.Namespace) -> None:
    """List out snapshots available to apply"""
    print(f"list of available snapshots at: {CONFIG_SNAPSHOT_DIR}")

    files = os.listdir(CONFIG_SNAPSHOT_DIR)
    files.sort(reverse=True)

    for num, file in enumerate(files):
        print(f"{num}: {file}")


def delete_snapshot(args: argparse.Namespace) -> None:
    """Delete by either filename or by index number"""
    try:
        snapshot = get_snapshot_by_rel(args.snapshot)

        print(f"removing snapshot: {snapshot}")

        if args.dry_run:
            print("dry-run")
        else:
            os.remove(snapshot)

    except IndexError:
        print_missing_snapshot_error(args)


def restore_snapshot(args: argparse.Namespace) -> None:
    """
    Apply a stored snapshot
    :param args:
    :return:
    """
    try:
        snapshot = get_snapshot_by_rel(args.snapshot)

        if args.no_backup:
            print("no-backup")
        else:
            create_snapshot(snapshot)

        if args.no_apply:
            print("no-apply")
        else:
            apply_snapshot(snapshot)
    except IndexError:
        print_missing_snapshot_error(args)


def print_missing_snapshot_error(args: argparse.Namespace) -> None:
    print(f"Error snapshot {args.snapshot} doesn't exist")
    print("Snapshots available are: ")
    main(args)
    print("\n")
    sys.exit(1)
