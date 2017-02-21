"""
    `mk-deps` - Cli tool for installing runtime dependencies of a debian package

    This module contains the core functionallity.

    :copyright: (c) by Livio Brunner
    :license: MIT, see LICENESE for details
"""
import re
import warnings
import logging
import apt
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

def try_install_package(pkg_name):
    """
    Tries to install the package using apt. If it fails, it
    returns false and logs the error.

    Args:
        pkg_name: The name of the package
    Returns:
        bool: If it was able to install
    """
    try:
        install_package(pkg_name)
    except apt.cache.LockFailedException:
        logging.warning("Could not install the package %s. Did you run with sudo?",
                        pkg_name)
        return False
    except KeyError:
        logging.warning("Package %s not found in cache.",
                        pkg_name)
        return False
    return True

def get_dependency_names(content, package_name=None):
    """
    Parses the dependencies of the package and returns
    them as a string array
    Args:
        content (str): The content of the package
        package_name (str): The name of the package, which
        dependency names should get returned
    Returns:
        list of str: The dependencies of the given file
    """
    pkgs = deb822.Packages.iter_paragraphs(content)
    dependencies = []
    for pkg in pkgs:
        # When "parsed correctly" AND if package_name is set, the package_name equals
        # the parsed packagename
        if pkg["package"] and (not package_name or package_name == pkg["package"]):
            rels = pkg.relations
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

def remove_variables(text):
    """
    Removes variables like ${misc:Depends}

    Args:
        text (str): The text to replace the variables
    Returns:
        str: The text without the variables
    """
    return re.sub(r"(\(.*\${.*}.*\))", "", text)

def is_variable(text):
    """
    Checks if the given string is a variable in the format
    ${*}

    Args:
        text (str): The text which should be checked
    Returns
        str: If the text contains a variable
    """
    return re.match(r"(\${.*})", text) is not None
def install_dependencies(control_file, package_name=None, dry_run=False):
    """
    Installs the dependencies of the given control file name.

    Args:
        control_file (str): The name of the debian/control file
        package_name (str): The name of the package which only should get installed from
        the control file
        dry_run (bool): Run the command without actually installing packages
    """
    warnings.simplefilter("ignore", UserWarning)
    file = open(control_file, "r")
    content = remove_variables(file.read())
    regex = r"^(Package:.+?(?=(Package:|\Z)))"
    matches = re.finditer(regex, content, re.MULTILINE | re.DOTALL)

    for _, match in enumerate(matches):
        dependencies = []
        dependencies = get_dependency_names(match.group(1), package_name)
        for dependency in dependencies:
            if isinstance(dependency, list):
                for or_dependency in dependency:
                    # If is not a variable..
                    if not is_variable(or_dependency):
                        if dry_run:
                            print(or_dependency)
                        else:
                            try_install_package(or_dependency)
            else:
                # If is not a variable..
                if not is_variable(dependency):
                    if dry_run:
                        print(dependency)
                    else:
                        try_install_package(dependency)
