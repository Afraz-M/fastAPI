import pytest
from app.calculations import add, subtract, multiply, divide


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1: int, num2: int, expected: int):
    print("testing add function")
    assert add(num1, num2) == expected


# def test_subtract():
#     assert subtract(8, 5) == 3


# test_add()
# test_subtract()
