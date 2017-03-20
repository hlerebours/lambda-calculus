""" Ensure all the Python snippets written as examples in the README actually work!
For that, we dynamically add a python test file inside this directory from the
snippets written in the README.rst.
The new file is only created when py.test is collecting the modules to test.
"""

import os
from collections import namedtuple
from itertools import takewhile

import setup
from lambdax import x


_Snippet = namedtuple('_Snippet', ('lineno', 'indent', 'lines'))


def _extract_snippets():
    python_block = None
    with open(os.path.join(os.path.dirname(setup.__file__), 'README.rst')) as f:
        for no, line in enumerate(f):
            if line.strip() and (".. code-block:: python" in line or python_block is not None):
                current_indent = sum(1 for _ in takewhile((x == ' ').β, line))
                if python_block is None:
                    # a code block starts here with an indentation greater than:
                    python_block = current_indent
                elif isinstance(python_block, _Snippet):
                    if current_indent >= python_block.indent:
                        # we're still in the last opened code block
                        python_block.lines.append(line[python_block.indent:])
                    else:
                        # end of the code block
                        python_block = None
                else:
                    assert current_indent > python_block, \
                        "Empty code block at line %d" % (no + 1)
                    python_block = _Snippet(no + 1, current_indent, [line.lstrip()])
                    yield python_block


def _create_snippets_file():
    snippets = list(_extract_snippets())
    assert snippets

    with open(os.path.join(os.path.dirname(__file__), 'test_readme_snippets.py'), 'w') as f:
        header = '""" Module generated to test the snippets in README.rst.\n' \
                 'It must not be committed.\n"""\n\n\n' \
                 'def test_all_snippets():  # pylint: disable=C0413\n'
        content = header + "\n".join(
            "    # Snippet %d (from line %d):\n    %s" % (
                i + 1,
                snippet.lineno,
                "    ".join(snippet.lines)
            )
            for i, snippet in enumerate(snippets)
        )
        print(content, end='', file=f)


def pytest_collect_directory(path, parent):
    """ Actual py.test hook to create the new test file when test modules are collected """
    if path == os.path.dirname(__file__):
        _create_snippets_file()
