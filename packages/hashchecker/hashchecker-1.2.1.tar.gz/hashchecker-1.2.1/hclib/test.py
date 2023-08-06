import textwrap
from os import path as os_path
from shutil import get_terminal_size

import click
import hclib.help_strings as hs
import pkg_resources
from colorama import Fore as fgc
from hclib.core.core_actions import calculate, find_duplicates, verify
from hclib.core.core_objects import CHECKSUMS, DirectoryObject, FileObject
from tabulate import tabulate


def get_files_dirs(arg_list):
    for arg in arg_list:
        if os_path.isfile(arg):
            yield FileObject(arg)
        elif os_path.isdir(arg):
            yield DirectoryObject(arg)
        else:
            print(f"- I did not find a file named '{arg}'")

cli()

@click.group(
    help=hs.cli_help,
)
@click.version_option(
    version=get_version(),
    prog_name="Hashchecker"
)
def cli():
    """
    Entry point for CLI commands
    """
    pass


@cli.command(
    'calculate',
    help=hs.calculate_help,
)
@click.argument(
    'arg_list',
    required=True,
    nargs=-1,
)
@click.option(
    '-c', '--checksum',
    'checksums',
    type=click.Choice(CHECKSUMS),
    default=['sha256'],
    multiple=True,
    help=hs.calculate_checksum_help,
)
@click.option(
    '-x', '--hidden',
    is_flag=True,
    help=hs.calculate_hidden_help,
)
@click.option(
    '-t', '--plaintext',
    is_flag=True,
    help=hs.plaintext_help,
)
def cli_calculate(arg_list, checksums, hidden, plaintext):
    """
    CLI Interface of the `calculate` command.

    First, files and directories are classified into separate lists. Missing
    files and directories are reported.
    """
    files, dirs = get_files_dirs(arg_list)
