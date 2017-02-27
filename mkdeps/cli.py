"""
    `mk-deps` - Cli tool for installing runtime dependencies of a debian package

    :copyright: (c) by Livio Brunner
    :license: MIT, see LICENESE for details
"""
import sys
import logging
import argparse
import argcomplete

from .core import install_dependencies, print_version
from .exit_status import ExitStatus


def main():
    """
    Install runtime dependencies of a debian package
    """
    exit_status = ExitStatus.SUCCESS
    parser = argparse.ArgumentParser(description="Install runtime dependencies")
    parser.add_argument("-i", "--install",
                        help="Install the generated packages and its runtime-dependencies.")

    parser.add_argument("-p", "--package",
                        help="Installs just the given package from the given control file")

    parser.add_argument("--version",
                        action="store_true",
                        help="Show version and copyright information.")

    parser.add_argument("--dry-run",
                        action="store_true",
                        help="Run the command without actually installing packages")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.version:
        print_version()

    if args.install and not args.dry_run:
        print("\033[94mInstalling runtime dependencies..\033[0m")
        exit_status = install_dependencies(args.install, args.package, False)
        print("\033[92mDone!\033[0m")

    if args.dry_run:
        if args.install:
            exit_status = install_dependencies(args.install, args.package, True)
        else:
            logging.warning("You must specify the debian/control file using the '--install'-option")

    sys.exit(exit_status)

if __name__ == '__main__':
    main()
