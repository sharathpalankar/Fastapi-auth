def add_twonumbers(x, y):
    return x + y

import pytest

def test_add_twonumbers():
    assert add_twonumbers(3, 5) == 8
    assert add_twonumbers(-1, 1) == 0
    assert add_twonumbers(0, 0) == 0