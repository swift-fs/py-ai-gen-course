# 第 17 章：测试

> **学习目标**：学会用 pytest 编写测试，掌握参数化测试和 fixture，养成写测试的习惯。

---

## 1. 为什么需要测试？

手动测试很慢、容易遗漏。**自动化测试**让代码变更有保障：

- 改代码后跑一下测试，确保没破坏已有功能
- 测试就是"活的文档"——展示代码应该怎么用
- 测试驱动开发（TDD）：先写测试，再写代码

---

## 2. pytest 基础

### 安装

```powershell
uv add --dev pytest
```

### 第一个测试

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
```

```python
# test_calculator.py
from calculator import add, divide

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    import pytest
    with pytest.raises(ValueError):
        divide(10, 0)
```

### 运行测试

```powershell
uv run pytest
uv run pytest -v              # 详细输出
uv run pytest test_file.py    # 指定文件
```

---

## 3. 参数化测试

用 `@pytest.mark.parametrize` 一次测试多组数据：

```python
import pytest
from calculator import add

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
    (-5, -3, -8),
])
def test_add_many(a, b, expected):
    assert add(a, b) == expected
```

---

## 4. fixture —— 测试夹具

fixture 提供测试所需的"准备工作"和"清理工作"：

```python
import pytest
from pathlib import Path

@pytest.fixture
def temp_file():
    """创建临时文件，测试后自动清理"""
    path = Path("test_temp.txt")
    path.write_text("测试数据", encoding="utf-8")
    yield path              # yield 之前是"准备"，之后是"清理"
    path.unlink(missing_ok=True)

def test_read_file(temp_file):
    content = temp_file.read_text(encoding="utf-8")
    assert content == "测试数据"
```

### fixture 的作用域

```python
@pytest.fixture(scope="function")  # 每个测试函数执行一次（默认）
def data():
    return [1, 2, 3]

@pytest.fixture(scope="module")    # 每个模块执行一次
def db_connection():
    print("连接数据库")
    yield "connection"
    print("断开数据库")

@pytest.fixture(scope="session")   # 整个测试会话执行一次
def config():
    return {"debug": True}
```

---

## 5. 测试覆盖率

```powershell
uv add --dev pytest-cov
uv run pytest --cov=calculator --cov-report=term-missing
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| `assert` | 断言条件为真 |
| `pytest.raises` | 测试异常 |
| `@pytest.mark.parametrize` | 参数化测试 |
| `@pytest.fixture` | 测试准备和清理 |
| `scope` | fixture 的生命周期 |
| `--cov` | 测试覆盖率 |

---

## 下一步

恭喜你完成了**进阶篇**！进入 [第 18 章：项目结构](../../03-python-practice/18-project-structure/README.md)，开始实战之旅。
