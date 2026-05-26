# conftest.py
import pytest


@pytest.fixture
def base_url():
    return "https://www.baidu.com"
