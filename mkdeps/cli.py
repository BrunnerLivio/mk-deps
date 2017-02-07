"""
    `mk-deps` - Cli tool for installing runtime dependencies of a debian package

    :copyright: (c) by Livio Brunner
    :license: MIT, see LICENESE for details
"""
import sys
import argparse
from .core import install_dependencies, print_version

def main():
    """
    Install runtime dependencies of a debian package
    """
    parser = argparse.ArgumentParser(description="Install runtime dependencies")
    parser.add_argument("-i", "--install",
                        help="Install the generated packages and its runtime-dependencies.")

    parser.add_argument("--version",
                        action="store_true",
                        help="Show version and copyright information.")

    parser.add_argument("--dry-run",
                        action="store_true",
                        help="Run the command without actually installing packages")

    args = parser.parse_args()

    if args.version:
        print_version()

    if args.install:
        install_dependencies(args.install)

    if args["dry-run"]:
        print("dry run")

    sys.exit()

if __name__ == '__main__':
    main()
