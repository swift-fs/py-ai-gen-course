# 第 17 章测试文件
# 运行方式：uv run pytest test_calculator.py -v
# 也可以直接运行：python test_calculator.py

import pytest
from calculator import add, divide


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
        (-5, -3, -8),
    ],
)
def test_add_many(a, b, expected):
    assert add(a, b) == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
