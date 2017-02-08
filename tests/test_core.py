import pytest

from mkdeps.core import get_dependency_names

def test_dep():
    """
    Test get_dependency_names() using a simple example of a debian
    package
    """
    text = """
Package: grml-live-db
Architecture: all
Depends: grml-live,
        libdbd-sqlite3-perl,
        libdbi-perl,
        libtimedate-perl,
        sqlite3,
        ${misc:Depends}
Recommends: perl-doc
Description: log package build information of grml-live to database
    """
    dependencies = get_dependency_names(text)
    assert len(dependencies) == 5
    assert "grml-live" in dependencies
    assert "libdbd-sqlite3-perl" in dependencies
    assert "libdbi-perl" in dependencies
    assert "libtimedate-perl" in dependencies
    assert "sqlite3" in dependencies

def test_dep_or():
    """
    Test get_dependency_names() using a OR-dependency-example of
    a debian package
    """
    text = """
Package: grml-live-db
Architecture: all
Depends: grml-live,
        libdbd-sqlite3-perl,
        libdbi-perl,
        libtimedate-perl | test,
        sqlite3,
        ${misc:Depends}
Recommends: perl-doc
Description: log package build information of grml-live to database
    """

    dependencies = get_dependency_names(text)
    assert isinstance(dependencies[3], list)
    assert dependencies[3][0] == "libtimedate-perl"
    assert dependencies[3][1] == "test"


