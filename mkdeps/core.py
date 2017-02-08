"""
    `mk-deps` - Cli tool for installing runtime dependencies of a debian package

    This module contains the core functionallity.

    :copyright: (c) by Livio Brunner
    :license: MIT, see LICENESE for details
"""
import re
import apt
import logging
from debian import deb822

from . import __VERSION__

def print_version():
    """
    Prints the version of the package and the license.
    """
    version_text = """
This is mk-deps, version {version}
Copyright (C) 2017 Livio Brunner

This program comes with ABSOLUTELY NO WARRANTY.
You are free to redistribute this code under the terms of the
GNU General Public License, version 2, or (at your option) any
later version.
    """.format(version=__VERSION__)
    print(version_text)

def install_package(pkg_name):
    """
    Installs the given package using apt.

    Args:
        pkg_name (str): The name of the package to install
    """
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[pkg_name]


    if pkg.is_installed:
        logging.info("%s already installed", pkg_name)

    else:
        logging.info("%s installing", pkg_name)
        pkg.mark_install()
        cache.commit()

def install_packages(deps, dry_run=False):
    """
    Installs all packages from the given array.
    If multiple dependecies options are given, it
    tries to install them one after another, until one succeeds
    Args:
        deps: List of dependecies
        dry_run (bool): Run the command without actually installing packages
    """
    if len(deps) == 1:
        pkg_name = deps[0]["name"]
        if pkg_name == "${misc:Depends}":
            return
        try:
            if dry_run:
                print(pkg_name)
            else:
                install_package(pkg_name)
        except Exception as exception: #pylint: disable=W0703
            logging.warning(str(exception))
    else:
        for index, dep in enumerate(deps):
            try:
                pkg_name = dep["name"]
                if index:
                    logging.info("Try installing %s instead",
                                 pkg_name)
                if dry_run:
                    print(pkg_name)
                else:
                    install_package(pkg_name)
                break
            except Exception as exception: #pylint: disable=W0703
                logging.warning(str(exception))

def parse_package(content, dry_run=False):
    """
    Parses the file and installs the runtime dependencies
    Args:
        content (str): The content of the package
        dry_run (bool): Run the command without actually installing packages
    """
    pkgs = deb822.Packages.iter_paragraphs(content)
    for pkg in pkgs:
        if pkg["package"]:
            name = pkg["package"]
            logging.info("==Installing packages of %s", pkg_name=name)
            rels = pkg.relations
            for deps in rels["depends"]:
                install_packages(deps, dry_run)

def install_dependencies(control_file, dry_run=False):
    """
    Installs the dependencies of the given control file name.

    Args:
        control_file (str): The name of the debian/control file
        dry_run (bool): Run the command without actually installing packages
    """
    file = open(control_file, "r")
    content = file.read()
    regex = r"^(Package:.+?(?=(Package:|\Z)))"
    matches = re.finditer(regex, content, re.MULTILINE | re.DOTALL)

    for _, match in enumerate(matches):
        parse_package(match.group(1), dry_run)
