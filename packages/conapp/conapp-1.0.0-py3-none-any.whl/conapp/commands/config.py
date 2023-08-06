import os
import argparse
import sys

from conapp.url_generators import RESOLVERS
from conapp.file_paths import get_repo_dir
from conapp.definitions import Hosts, PROGRAM_NAME
from conapp.file_paths import check_dirs, create_dirs, get_config_dir, CONFIG_REPO_DIR,REPO_DIR
from conapp.file_ops import apply_snapshot, create_snapshot, download_file, \
    apply_config, get_files_from_tar

BACKUP_FILE_NAME = "backup.tar.gz"

COMMAND = 'config'
COMMAND_HELP = "manage downloading and applying configs"


def setup_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Setup the arguments for the config command
    """
    parser.set_defaults(command=lambda x: parser.print_usage())

    subparsers = parser.add_subparsers(
        title=f"{COMMAND} commands",
        description="sub commands for managing configs"
    )

    apply_parser = subparsers.add_parser(
        'apply',
        help='download and apply a config from github or bitbucket'
    )

    apply_parser.set_defaults(command=main)

    apply_parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='username to pull from'
    )
    apply_parser.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )
    apply_parser.add_argument(
        '--no-download',
        action='store_true',
        help='Use already downloaded copy'
    )
    apply_parser.add_argument(
        '-b',
        '--bitbucket',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.BITBUCKET,
        help='pull from bitbucket'
    )
    apply_parser.add_argument(
        '-g',
        '--github',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.GITHUB,
        help='pull from bitbucket'
    )
    apply_parser.add_argument(
        '--no-apply',
        action="store_true",
        dest="no_apply",
        help="Don't actually run"
    )

    list_parser = subparsers.add_parser('list', help="list downloaded configs")

    list_parser.set_defaults(command=list_configs)

    list_parser.add_argument(
        '-u',
        '--user',
        help='username to pull from'
    )

    undo_parser = subparsers.add_parser(
        'undo',
        help='Restore the snapshot taken when config was last applied'
    )

    undo_parser.set_defaults(command=undo_config)

    undo_parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='username to pull from'
    )
    undo_parser.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )

    return parser


def main(args: argparse.Namespace) -> None:
    """Download and Apply a snapshot"""
    repo_dir = get_repo_dir(args.user, args.repo)

    if not check_dirs([repo_dir]):
        create_dirs([repo_dir])

    file_name = os.path.join(
        repo_dir,
        f"{args.user}.{args.repo}.tar.gz"
    )

    if args.no_download and os.path.isfile(file_name):
        print(f"no-download passed, applying local file {file_name}")
    else:
        if args.no_download:
            print("Error: no-download passed but no local copy to apply!")
            sys.exit(2)
        else:
            download_file(
                file_name,
                RESOLVERS.get(args.host)(args.user, args.repo)
            )

    if args.no_apply:
        print(f"--no-apply passed, not applying {file_name}")
    else:
        snapshot = create_snapshot(file_name)
        link_name = os.path.join(repo_dir, BACKUP_FILE_NAME)

        if os.path.isfile(link_name):
            os.remove(link_name)

        os.link(
            snapshot,
            link_name
        )

        if input("About to override files, really apply? [y/N]: ") == 'y':
            apply_config(file_name)
            print("config applied successfully.\nYou can undo this by running:")
            print(f"{PROGRAM_NAME} config undo -u {args.user} -r {args.repo}")
        else:
            print(f"Not applying {file_name}")


def list_configs(args: argparse.Namespace) -> None:
    users = {}

    # NOTE: This could probably be done with os.walk and save some fs calls
    #  however there would be a bunch of additional checking needed to be done since its a flat list instead of nested w
    for user_dir in os.scandir(CONFIG_REPO_DIR):
        if user_dir.is_dir():
            repos = []

            for user_repo_dir in os.scandir(user_dir.path):
                if user_repo_dir.is_dir \
                        and (f"{user_dir.name}.{user_repo_dir.name}.tar.gz" in os.listdir(user_repo_dir.path)):
                    repos.append(user_repo_dir.name)

            if len(repos) > 0:
                users[user_dir.name] = repos

    if args.user is not None:
        if args.user in users:
            print_user(args.user, users[args.user])
            print(get_repo_dir(args.user, users[args.user][0]))
        else:
            print(f"user {args.user} has no downloaded configs")
    else:
        print("Downloaded configs are: \n")
        for user, repos in users.items():
            print_user(user, repos)
            print("")


def print_user(user: str, repos: list) -> None:
    print(f"- {user}:")
    for repo in repos:
        print(f"  * {repo}")


def undo_config(args: argparse.Namespace) -> None:
    repo_dir = get_repo_dir(args.user, args.repo)
    backup_name = os.path.join(
        repo_dir,
        BACKUP_FILE_NAME
    )
    config_file_name = os.path.join(
        repo_dir,
        f"{args.user}.{args.repo}.tar.gz"
    )

    if input("Create a backup before undo?: ") == 'y':
        create_snapshot(config_file_name)

    if input(f"Remove all files pointed to by {config_file_name} before restore?: ") == 'y':
        files = filter(
            lambda file_path: os.path.isfile(os.path.expanduser(f"~/{file_path}")),
            get_files_from_tar(config_file_name, True).stdout.split()
        )

        for file in files:
            path = f"~/{file}"
            print(f"removing {path}")
            os.remove(os.path.expanduser(path))

    if os.path.isfile(backup_name) \
            and input(f"about to restore {backup_name}\nContinue? [y/N]") == 'y':
        apply_snapshot(backup_name)
    else:
        print(f"No backup found at: {backup_name}")
