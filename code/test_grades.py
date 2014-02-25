import grades

def test_get_level():
    assert grades.get_level(2, 5) == 'elementary'


import pytest
import sys

@pytest.mark.slow
def test_slow():
    assert True


@pytest.mark.crappy
def test_crappy():
    assert True


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows specific')
def test_updates_registry():
    assert False


@pytest.mark.xfail
def test_foo():
    assert True
