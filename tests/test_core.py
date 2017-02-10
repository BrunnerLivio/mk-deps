import pytest

from mkdeps.core import get_dependency_names, remove_variables, is_variable

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

def test_remove_variables():
    """
    Test remove_variables() method by using
    an example string
    """
    input_text = "Depends: (>= ${source:Version})"
    output_text = remove_variables(input_text)
    assert output_text == "Depends: "

def test_is_variable():
    """
    Test is_variable() method by using
    an example string
    """
    input_text = "${misc:Depends}"
    assert is_variable(input_text)
    input_text = "grml-live"
    assert not is_variable(input_text)
