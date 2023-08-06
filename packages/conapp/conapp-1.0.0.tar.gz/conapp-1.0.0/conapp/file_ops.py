import subprocess
import os
import urllib.request
import sys

from typing import Optional
from conapp.file_paths import get_snapshot_filename
from conapp.validate import validate_subprocess
from conapp.definitions import USER_HOME_DIR, DEFAULT_STRIP_COMPONENTS


def apply_config(file_name: str) -> None:
    """
    A wrapper around apply snapshot but for stripping the top level
    :param file_name:
    :return:
    """
    return apply_snapshot(file_name, True)


def apply_snapshot(file_name: str, strip_top_level=False) -> None:
    """Given file_name use tar to apply it to the users home directory"""
    if not os.path.isfile(file_name):
        print(f"Error! attempted to apply nonexistent snapshot {file_name}")

    print(f"Applying snapshot {file_name}")

    validate_subprocess(
        subprocess.run([
            'tar',
            '-C',
            USER_HOME_DIR,
            DEFAULT_STRIP_COMPONENTS if strip_top_level else '',
            '--show-transformed-names',
            '-zvxf',
            file_name,
        ])
    )


def create_snapshot(file_name: str) -> Optional[str]:
    file_names_result = get_files_from_tar(file_name, True)

    files = list(
        filter(
            lambda file_path: os.path.isfile(os.path.expanduser(f"~/{file_path}")),
            file_names_result.stdout.split()
        )
    )

    if len(files) > 0:
        snapshot_name = get_snapshot_filename()
        backup_command = [
                             'tar',
                             '-C',
                             USER_HOME_DIR,
                             '-czvf',
                             snapshot_name,
                         ] + files

        print(f"Local files would get overridden, creating backup of: {' '.join(files)}")

        validate_subprocess(subprocess.run(
            backup_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        ))

        print(f"Successfully backed up files to {snapshot_name}")
        return snapshot_name

    else:
        print("No files will be overridden, not creating backup")
        return None


def get_files_from_tar(file_name: str, strip_top_level=False) -> subprocess.CompletedProcess:
    get_file_names_command = [
        "tar",
        DEFAULT_STRIP_COMPONENTS if strip_top_level else '',
        '--show-transformed-names',
        '-tf',
        file_name
    ]
    result = subprocess.run(
        get_file_names_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    validate_subprocess(result)

    return result


def download_file(file_name: str, url: str) -> None:
    """Attempt to download a file or exit"""

    try:
        print(f"Attempting to download {url}")
        urllib.request.urlretrieve(url, file_name)
        print(f"Success, downloaded to {file_name}")
    except urllib.request.HTTPError as ex:
        print(f"Error occurred, does {url} exist?\n{ex}")
        sys.exit(-1)
