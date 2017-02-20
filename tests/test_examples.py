"""
Test real examples (blackbox test). Compares the input files from test/input folder
with the reference files test/refs folder.
"""
import os
import pytest # pylint: disable=unused-import

from mkdeps.core import install_dependencies

CWD = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = os.path.join(CWD, "input")
REFS_PATH = os.path.join(CWD, "refs")

def test_examples(capsys):
    """
    Test real examples. Compares the input files from test/input folder
    with the reference files test/refs folder.
    """
    examples = os.listdir(INPUT_PATH)
    for example in examples:
        install_dependencies(os.path.join(INPUT_PATH, example), None, True)

        result_string, _ = (capsys.
                            readouterr())
        result_string = (result_string.
                         strip().
                         replace('\n', '').
                         replace(' ', ''))

        file = open(os.path.join(REFS_PATH, example), "r")

        expected_string = (file.
                           read().
                           strip().
                           replace('\n', '').
                           replace(' ', ''))
        assert result_string == expected_string
