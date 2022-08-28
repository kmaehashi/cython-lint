import pytest

from cython_lint import main
import os

INCLUDE_FILE = os.path.join('tests', 'data', 'foo.pxi')

@pytest.mark.parametrize(
    'src, expected',
    [
        (
            'cdef bint foo():\n'
            '    cdef int a\n',
            't.py:2:13: \'a\' defined but unused\n'
        ),
    ]
)
def test_assigned_unused(capsys, src, expected):
    ret = main(src, 't.py')
    out, _ = capsys.readouterr()
    assert out == expected
    assert ret == 1

@pytest.mark.parametrize(
    'src, expected',
    [
        (
            'cimport foo\n',
            't.py:1:9: Name foo imported but unused\n',
        ),
        (
            'from foo cimport bar\n',
            't.py:1:18: Name bar imported but unused\n',
        ),
        (
            'from foo import bar, bar2\n',
            't.py:1:17: Name bar imported but unused\n'
            't.py:1:22: Name bar2 imported but unused\n',
        ),
    ]
)
def test_imported_unused(capsys, src, expected):
    ret = main(src, 't.py')
    out, _ = capsys.readouterr()
    assert out == expected
    assert ret == 1

@pytest.mark.parametrize(
    'src',
    [
            'cdef bint foo():\n'
            '    raise NotImplemen',
            'cdef bint foo():\n'
            '    cdef int i\n'
            '    for i in bar: pass\n',
            'cdef bint foo(a):\n'
            '   pass\n',
            'cdef bint foo(int a):\n'
            '   pass\n',
            'cdef bint foo(int *a):\n'
            '   pass\n',
            'cdef bint* foo(int a):\n'
            '   pass\n',
            'cdef bint foo():\n'
            '    cdef int i\n'
            '    for i, j in bar: pass\n',
            'cdef bint foo(object (*operation)(int64_t value, object right)):\n'
            '   pass\n',
            'import numpy as np\n',  # todo: should detect this
            'class Foo: pass\n',
            'cdef class Foo: pass\n',
            'cdef bint foo(a):\n'
            '    bar(<int>a)\n',
            'cdef bint foo(a):\n'
            '    bar(i for i in a)\n',
            'cdef bint foo(a):\n'
            '    bar(lambda x: x)\n',
            'import int64_t\n'
            'ctypedef fused foo:\n'
            '    int64_t\n'
            '    int32_t\n',
            'import quox\n'
            f'include "{INCLUDE_FILE}"\n'
    ]
)
def test_noop(capsys, src):
    ret = main(src, 't.py')
    out, _ = capsys.readouterr()
    assert out == ''
    assert ret == 0