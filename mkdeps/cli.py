"""
    `mk-deps` - Cli tool for installing runtime dependencies of a debian package

    :copyright: (c) by Livio Brunner
    :license: See LICENESE for details
"""
import sys
import logging
import click

from .core import install_dependencies, print_version
from .exit_status import ExitStatus

@click.group()
@click.option("--version",
              count=True,
              default=False,
              help="Show version and copyright information")
def cli(version):
    """
    Install runtime dependencies of a debian package
    """
    if version:
        print_version()

@cli.command()
@click.option("--package",
              help="Installs just the given package from the given control file")
@click.option("--dry-run",
              count=True,
              default=False,
              help="Run the command without actually installing packages")
@click.argument("control_file")
def install(package, dry_run, control_file):
    """
    Install runtime-dependencies a debian package
    """

    exit_status = ExitStatus.SUCCESS

    print("\033[94mInstalling runtime dependencies..\033[0m")
    exit_status = install_dependencies(control_file, package, dry_run)
    print("\033[92mDone!\033[0m")

    sys.exit(exit_status)
