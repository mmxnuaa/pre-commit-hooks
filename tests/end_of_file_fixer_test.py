from __future__ import annotations

import io

import pytest

from pre_commit_hooks.end_of_file_fixer import fix_file
from pre_commit_hooks.end_of_file_fixer import main


# Input, expected return value, expected output
TESTS = (
    (b'foo\n', 0, b'foo\n'),
    (b'', 0, b''),
    (b'\n\n', 1, b''),
    (b'\n\n\n\n', 1, b''),
    (b'foo', 1, b'foo\n'),
    (b'foo\n\n\n', 1, b'foo\n'),
    (b'\xe2\x98\x83', 1, b'\xe2\x98\x83\n'),
    (b'foo\r\n', 0, b'foo\r\n'),
    (b'foo\r\n\r\n\r\n', 1, b'foo\r\n'),
    (b'foo\r', 0, b'foo\r'),
    (b'foo\r\r\r\r', 1, b'foo\r'),
)

TESTS_MAIN = (
    (b'foo\n', 0, b'foo\n', None),
    (b'', 0, b'', None),
    (b'\n\n', 1, b'', None),
    (b'\n\n\n\n', 1, b'', None),
    (b'foo', 1, b'foo\n', None),
    (b'foo\n\n\n', 1, b'foo\n', None),
    (b'\xe2\x98\x83', 1, b'\xe2\x98\x83\n', None),
    (b'foo\r\n', 0, b'foo\r\n', None),
    (b'foo\r\n\r\n\r\n', 1, b'foo\r\n', None),
    (b'foo\r', 0, b'foo\r', None),
    (b'foo\r\r\r\r', 1, b'foo\r', None),

    (b'foo\n', 0, b'foo\n', '--exit-zero'),
    (b'', 0, b'', '--exit-zero'),
    (b'\n\n', 0, b'', '--exit-zero'),
    (b'\n\n\n\n', 0, b'', '--exit-zero'),
    (b'foo', 0, b'foo\n', '--exit-zero'),
    (b'foo\n\n\n', 0, b'foo\n', '--exit-zero'),
    (b'\xe2\x98\x83', 0, b'\xe2\x98\x83\n', '--exit-zero'),
    (b'foo\r\n', 0, b'foo\r\n', '--exit-zero'),
    (b'foo\r\n\r\n\r\n', 0, b'foo\r\n', '--exit-zero'),
    (b'foo\r', 0, b'foo\r', '--exit-zero'),
    (b'foo\r\r\r\r', 0, b'foo\r', '--exit-zero'),
)


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output'), TESTS)
def test_fix_file(input_s, expected_retval, output):
    file_obj = io.BytesIO(input_s)
    ret = fix_file(file_obj)
    assert file_obj.getvalue() == output
    assert ret == expected_retval


@pytest.mark.parametrize(('input_s', 'expected_retval', 'output', 'options'), TESTS_MAIN)
def test_integration(input_s, expected_retval, output, options, tmpdir):
    path = tmpdir.join('file.txt')
    path.write_binary(input_s)

    if options is None:
       options = []
    elif isinstance(options, str):
        options = [options]

    ret = main([*options, str(path)])
    file_output = path.read_binary()

    assert file_output == output
    assert ret == expected_retval
