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

def get_dependency_names(content):
    """
    Parses the dependencies of the package and returns 
    them as a string array
    Args:
        content (str): The content of the package
    Returns:
        list of str: The dependencies of the given file
    """
    pkgs = deb822.Packages.iter_paragraphs(content)
    for pkg in pkgs:
        if pkg["package"]:
            rels = pkg.relations
            dependencies = []
            for deps in rels["depends"]:
                if len(deps) == 1:
                    pkg_name = deps[0]["name"]
                    if pkg_name != "${misc:Depends}":
                        dependencies.append(pkg_name)
                else:
                    or_dependencies = []
                    for dep in deps:
                        pkg_name = dep["name"]
                        or_dependencies.append(pkg_name)
                    dependencies.append(or_dependencies)
    return dependencies

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
        dependencies = get_dependency_names(match.group(1))
        for dependency in dependencies:
            if isinstance(dependency, list):
                for or_dependency in dependency:
                    if dry_run:
                        print(or_dependency)
                    else:
                        try:
                            install_package(or_dependency)
                            break
                        except Exception:
                            logging.warning("Could not install the package %s",
                                            or_dependency)
            else:
                if dry_run:
                    print(dependency)
                else:
                    try:
                        install_package(dependency)
                    except Exception:
                        logging.warning("Could not install the package %s",
                                        dependency)
