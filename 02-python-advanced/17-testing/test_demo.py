from pathlib import Path
from demo import do_sum, do_divide, do_float_sum
import pytest


def test_do_sum():
    assert do_sum(1, 2, 3) == 6
    assert do_sum(4, 5, 6) == 15
    assert do_sum(1, 2, 3, 4, 5) == 15
    assert do_sum(0, 0, 0) == 0


def test_do_divide():
    assert do_divide(10, 2) == 5
    assert do_divide(15, 3) == 5
    with pytest.raises(ValueError, match="除数不能为0"):
        do_divide(10, 0)


def test_do_float_sum():
    assert do_float_sum(0.1, 0.2) == pytest.approx(0.3, abs=0.00001)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (-4, -5, -9),
        (0, 0, 0),
        pytest.param(10, 20, 40, marks=pytest.mark.skip()),
    ],
)
def test_do_sum_manay(a, b, expected):
    assert do_sum(a, b) == expected


@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5, 6, 7]


def test_do_sum_with_sample_data(sample_data):
    assert do_sum(*sample_data) == 28


@pytest.fixture
def temp_file():
    """创建临时文件，测试后自动清理"""
    path = Path("test_temp.txt")
    path.write_text("测试数据", encoding="utf-8")
    yield path  # yield 之前：准备阶段；之后：清理阶段
    path.unlink(missing_ok=True)


def test_read_file(temp_file):
    content = temp_file.read_text(encoding="utf-8")
    assert content == "测试数据"


def test_homepage(base_url):
    assert base_url == "https://www.baidu.com"
