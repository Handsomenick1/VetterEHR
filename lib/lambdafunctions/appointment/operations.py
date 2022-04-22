import pytest

def test_success():
    """this test succeeds"""
    print(1)
    assert True
def test_failure():
    print(2)
    """this test fails"""
    assert False
def test_skip():
    print(3)
    """this test is skipped"""
    pytest.skip('for a reason!')
def test_broken():
    raise Exception('oops')
def test_success2():
    print(4)
    assert True