import os
import argparse
import subprocess
import shutil

from conapp.file_paths import CONFIG_TRACK_DIR
from conapp.validate import validate_subprocess
from conapp.url_generators import CHECKOUT_RESOLVERS
from conapp.definitions import Hosts, PROGRAM_NAME

COMMAND = "local"
COMMAND_HELP = "Command for managing a local repo"

TRACK_REPO_FOLDER_NAME = "repo"
REPO_FOLDER = os.path.join(CONFIG_TRACK_DIR, TRACK_REPO_FOLDER_NAME)


def setup_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(command=lambda x: parser.print_usage())

    sub_parser = parser.add_subparsers()

    checkout_parser = sub_parser.add_parser(
        "checkout",
        help="Checkout a repo locally and bare"
    )
    checkout_parser.set_defaults(command=checkout_command)

    checkout_parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='username to pull from'
    )
    checkout_parser.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )
    checkout_parser.add_argument(
        '-b',
        '--bitbucket',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.BITBUCKET,
        help='pull from bitbucket'
    )
    checkout_parser.add_argument(
        '-g',
        '--github',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.GITHUB,
        help='pull from bitbucket'
    )

    alias_parser = sub_parser.add_parser(
        "alias",
        help="Get info about the local repo"
    )

    alias_parser.set_defaults(
        command=alias_command
    )
    alias_parser.add_argument(
        "-d",
        "--details",
        help="Print some details on how to use the bare repo",
        action="store_true"
    )
    alias_parser.add_argument(
        "--alias-name",
        default="config",
        help="name for the alias to export"
    )

    return parser


def checkout_command(args: argparse.Namespace) -> None:
    """
    Checkout a "bare" repo for local setup
    :param args:
    :return:
    """
    if os.path.exists(REPO_FOLDER):
        if input("Repo folder is not empty, delete to continue? [y/N]:").lower() == "y":
            shutil.rmtree(REPO_FOLDER, True)
        else:
            print(f"Repo dir not empty, aborting.\nRepo dir = {REPO_FOLDER}")
            return

    command = [
        'git',
        'clone',
        '--bare',
        CHECKOUT_RESOLVERS.get(args.host)(args.user, args.repo),
        REPO_FOLDER,
    ]

    untrack_command = [
        'git',
        f"--git-dir={REPO_FOLDER}",
        'config',
        '--local',
        'status.showUntrackedFiles',
        'no'
    ]

    print(f"about to execute '{' '.join(command)}'")

    if input("Proceed [y/N]? ").lower() == "y":
        validate_subprocess(
            subprocess.run(command)
        )
        # TODO: Add an flag check around this
        validate_subprocess(
            subprocess.run(untrack_command)
        )

        print(f"\nYou can run `{PROGRAM_NAME} {COMMAND} alias --details` to get more info on"
              f" how to use your bare repository.\n")
    pass


def alias_command(args: argparse.Namespace) -> None:
    # TODO: Add output of what to do next (ie call `conapp local env`) to
    #  setup local stuff. Need to do more than bash eventually
    if not os.path.exists(REPO_FOLDER):
        print("You haven't checked out a repo yet!\n"
              f"see `{PROGRAM_NAME} {COMMAND} checkout` for more info")
        return

    alias_command = f"alias {args.alias_name}='git --work-tree={os.path.expanduser('~/')} --git-dir={os.path.abspath(REPO_FOLDER)}'"

    if args.details:
        print(
            "You have checked out a repo as a bare repository! "
            "This allows you to manage a repo with a working dir that is not next "
            "to the git directory. Essentially this lets us use git to manage our "
            "home folder without having a .git at the top level of it.\n\n"
            "See https://www.atlassian.com/git/tutorials/dotfiles for a great rundown on how this works\n\n"
            "If you rerun this command without the --details flag, it will print"
            " an alias for use in shells that will allow you to use the bare repo"
            " without all the extra flags being passed to git. IE:\n"
            f"`{args.alias_name} status`"
        )
    else:
        print(alias_command)
    pass
