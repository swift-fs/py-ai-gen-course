# 第 17 章：测试

> **学习目标**：学会用 pytest 编写测试，掌握断言、参数化测试、fixture 和常用标记，养成写测试的习惯。

---

## 1. 为什么需要测试？

手动测试很慢、容易遗漏。**自动化测试**让代码变更有保障：

- 改代码后跑一下测试，确保没破坏已有功能（**回归测试**）
- 测试就是"活的文档"——展示代码应该怎么用
- 测试驱动开发（TDD）：先写测试，再写代码，用测试来驱动设计

测试通常分三层：

| 类型       | 测什么        | 速度 |
| ---------- | ------------- | ---- |
| 单元测试   | 单个函数/方法 | 极快 |
| 集成测试   | 多个模块协作  | 较慢 |
| 端到端测试 | 整个应用流程  | 最慢 |

本章聚焦**单元测试**，使用的工具是 Python 社区最受欢迎的 **pytest**。

---

## 2. 安装与第一个测试

### 安装

```powershell
uv add --dev pytest
```

### 被测代码

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
```

### 编写测试

pytest 的测试发现规则：
- 文件名以 `test_` 开头，或以 `_test.py` 结尾
- 函数名以 `test_` 开头
- 类名以 `Test` 开头（类中的方法也要以 `test_` 开头）

```python
# test_calculator.py
from calculator import add, divide

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

就这么简单——**一个 `assert` 就是一个测试**。不需要继承任何基类，不需要特殊的断言方法。

### 运行测试

```powershell
uv run pytest                  # 运行所有测试
uv run pytest -v               # 详细输出（显示每个测试函数名）
uv run pytest test_calculator.py  # 指定文件
uv run pytest test_calculator.py::test_add  # 指定某个测试函数
uv run pytest -q               # 简洁输出（只显示 . F E 等符号）
uv run pytest -x               # 遇到第一个失败就停止
uv run pytest --tb=short       # 简短的错误回溯
```

pytest 的失败输出非常友好，它会告诉你**哪一行断言失败**、**实际值和期望值分别是什么**：

```
>       assert add(1, 2) == 4
E       assert 3 == 4
E        +  where 3 = add(1, 2)

test_calculator.py:5: AssertionError
```

---

## 3. 断言详解

断言是测试的核心。pytest 对 Python 原生 `assert` 做了增强，失败时提供详细的信息。

### 3.1 基本断言

```python
def test_assertions():
    # 比较相等
    assert 1 + 1 == 2
    assert "hello" != "world"

    # 布尔判断
    assert True
    assert not False

    # 包含关系
    assert 3 in [1, 2, 3]
    assert "lo" in "hello"

    # 类型检查
    assert isinstance(42, int)
```

### 3.2 测试异常：pytest.raises

当代码**应该抛出异常**时，用 `pytest.raises` 来验证：

```python
import pytest
from calculator import divide

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

还可以进一步检查异常信息：

```python
def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(10, 0)
```

`match` 参数接受正则表达式。如果异常信息不匹配，测试会失败。

### 3.3 测试警告：pytest.warns

和 `pytest.raises` 类似，用来测试代码是否发出了预期的警告：

```python
import pytest
import warnings

def warn_if_negative(value):
    if value < 0:
        warnings.warn("值为负数", UserWarning)
    return value

def test_warns():
    with pytest.warns(UserWarning, match="值为负数"):
        warn_if_negative(-1)
```

### 3.4 浮点数比较：pytest.approx

浮点数运算有精度问题，直接 `==` 比较往往会失败：

```python
# 这会失败！
# assert 0.1 + 0.2 == 0.3

import pytest

def test_float():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

`pytest.approx` 默认使用相对容差 `1e-9`，也可以手动指定：

```python
def test_float_tolerance():
    # 绝对容差：差值不超过 0.01 就算相等
    assert 1.001 == pytest.approx(1.0, abs=0.01)

    # 也可以比较列表中的浮点数
    assert [1.0, 2.0] == pytest.approx([1.0001, 1.9999], abs=0.001)
```

---

## 4. 参数化测试：@pytest.mark.parametrize

当你需要用**多组数据**测试同一个逻辑时，不想写多个测试函数，可以用参数化：

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

运行时 pytest 会为每一组数据生成一个独立的测试用例：

```
test_add_many[1-2-3] PASSED
test_add_many[-1-1-0] PASSED
test_add_many[0-0-0] PASSED
test_add_many[100-200-300] PASSED
test_add_many[-5--3--8] PASSED
```

### 给参数组起名字：ids

默认的测试名由参数值拼接而成，不太直观。可以用 `ids` 自定义：

```python
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("hello", "HELLO"),
        ("World", "WORLD"),
        ("", ""),
    ],
    ids=["小写转大写", "首字母大写转大写", "空字符串"]
)
def test_upper(input_str, expected):
    assert input_str.upper() == expected
```

### 对单组参数做标记：pytest.param

有时你想对某组参数单独标记为"预期失败"或"跳过"：

```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    pytest.param(10, 0, None, marks=pytest.mark.xfail(reason="除零应失败")),
    (0, 0, 0),
])
def test_add_special(a, b, expected):
    if b == 0:
        raise ValueError
    assert add(a, b) == expected
```

### 多个参数化装饰器（笛卡尔积）

多个 `@pytest.mark.parametrize` 会产生**笛卡尔积**：

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    # 会运行 4 次：(1,10), (1,20), (2,10), (2,20)
    assert x * y > 0
```

---

## 5. fixture —— 测试夹具

fixture 是 pytest 最强大的特性之一。它可以：
- 为测试提供**准备数据**
- 在测试后自动**清理资源**
- 在多个测试之间**共享状态**

### 5.1 基本 fixture

```python
import pytest

@pytest.fixture
def sample_data():
    """提供一组测试数据"""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_length(sample_data):
    assert len(sample_data) == 5
```

测试函数的参数名如果和某个 fixture 同名，pytest 会**自动注入**该 fixture 的返回值。

### 5.2 带 setup/teardown 的 fixture

使用 `yield` 可以在测试前后分别执行"准备"和"清理"：

```python
import pytest
from pathlib import Path

@pytest.fixture
def temp_file():
    """创建临时文件，测试后自动清理"""
    path = Path("test_temp.txt")
    path.write_text("测试数据", encoding="utf-8")
    yield path              # yield 之前：准备阶段；之后：清理阶段
    path.unlink(missing_ok=True)

def test_read_file(temp_file):
    content = temp_file.read_text(encoding="utf-8")
    assert content == "测试数据"
```

无论测试成功还是失败，**清理代码一定会执行**。

### 5.3 fixture 的作用域：scope

| scope 值           | 生命周期         | 适用场景                   |
| ------------------ | ---------------- | -------------------------- |
| `function`（默认） | 每个测试函数一次 | 每个测试需要独立的数据     |
| `class`            | 每个测试类一次   | 类中多个方法共享状态       |
| `module`           | 每个测试文件一次 | 文件内共享数据库连接等     |
| `package`          | 每个包一次       | 包内多个模块共享           |
| `session`          | 整个测试会话一次 | 全局配置、昂贵资源的初始化 |

```python
@pytest.fixture(scope="module")
def db_connection():
    """整个模块共享一个连接"""
    print("连接数据库")
    conn = create_connection()
    yield conn
    print("断开数据库")
    conn.close()
```

scope 越大，fixture 执行次数越少，性能越好，但**状态隔离性越差**。一般从 `function` 开始，有性能需要时再扩大。

### 5.4 fixture 依赖其他 fixture

fixture 可以像测试函数一样，通过参数名引用其他 fixture：

```python
@pytest.fixture
def user_data():
    return {"name": "张三", "age": 25}

@pytest.fixture
def user_with_id(user_data):
    """基于 user_data 扩展"""
    return {**user_data, "id": 1}

def test_user(user_with_id):
    assert user_with_id["id"] == 1
    assert user_with_id["name"] == "张三"
```

pytest 会自动解析依赖关系，按正确顺序执行。

### 5.5 自动使用：autouse

如果想让某个 fixture **自动应用**到所有测试，不需要手动声明参数：

```python
@pytest.fixture(autouse=True)
def reset_global_state():
    """每个测试前后自动重置全局状态"""
    global_state.clear()
    yield
    global_state.clear()
```

> **注意**：`autouse` 要谨慎使用，因为它会影响所有测试，可能带来意料之外的副作用。

### 5.6 conftest.py —— 共享 fixture

当多个测试文件需要用到同一个 fixture 时，把它放在 `conftest.py` 中：

```
project/
├── conftest.py          # 所有测试文件共享的 fixture
├── test_a.py
└── test_b.py
```

```python
# conftest.py
import pytest

@pytest.fixture
def base_url():
    return "http://localhost:8000"
```

```python
# test_a.py
def test_home(base_url):
    assert base_url == "http://localhost:8000"
```

```python
# test_b.py
def test_api(base_url):
    assert "/api" in f"{base_url}/api"
```

pytest 会**自动发现** `conftest.py` 中的 fixture，不需要手动 import。

> `conftest.py` 放在哪个目录，它的 fixture 就对那个目录及子目录的测试可见。

---

## 6. 常用标记：Marks

标记（mark）用来给测试附加元数据，控制测试的执行行为。

### 6.1 跳过测试：@pytest.mark.skip

```python
@pytest.mark.skip(reason="等待修复 bug #123")
def test_broken_feature():
    ...
```

### 6.2 条件跳过：@pytest.mark.skipif

```python
import sys

@pytest.mark.skipif(sys.platform == "win32", reason="Linux 专用测试")
def test_linux_feature():
    ...
```

### 6.3 预期失败：@pytest.mark.xfail

标记一个测试**预期会失败**。如果它确实失败了，结果记为 `XFAIL`（不算失败）；如果意外通过了，记为 `XPASS`：

```python
@pytest.mark.xfail(reason="这个 bug 还没修")
def test_known_bug():
    assert 1 == 2
```

### 6.4 自定义标记

你可以定义自己的标记，然后用 `-m` 选项筛选运行：

```python
@pytest.mark.slow
def test_large_dataset():
    # 处理大数据集，耗时较长
    ...
```

```powershell
# 只运行标记为 slow 的测试
uv run pytest -m slow

# 运行除了 slow 以外的所有测试
uv run pytest -m "not slow"
```

自定义标记需要在配置文件中注册（否则 pytest 会发出警告）。在 `pyproject.toml` 中添加：

```toml
[tool.pytest.ini_options]
markers = [
    "slow: 标记耗时较长的测试",
    "integration: 集成测试",
]
```

---

## 7. 用类组织测试

当一组测试共享相同的主题时，可以用类来组织：

```python
class TestAdd:
    def test_positive(self):
        assert add(1, 2) == 3

    def test_negative(self):
        assert add(-1, -2) == -3

    def test_zero(self):
        assert add(0, 0) == 0


class TestDivide:
    def test_normal(self):
        assert divide(10, 2) == 5.0

    def test_by_zero(self):
        with pytest.raises(ValueError):
            divide(1, 0)
```

> pytest 的测试类**不需要继承任何基类**（不要继承 `unittest.TestCase`，那样就失去 pytest 的优势了）。

---

## 8. 测试覆盖率

覆盖率衡量"你的测试执行了多少比例的代码"：

```powershell
uv add --dev pytest-cov
uv run pytest --cov=calculator           # 显示覆盖率百分比
uv run pytest --cov=calculator --cov-report=term-missing  # 显示未覆盖的行号
```

输出示例：

```
Name            Stmts   Miss  Cover   Missing
---------------------------------------------
calculator.py      10      2    80%   15-16
```

> 覆盖率是参考指标，**不是目标**。追求 100% 覆盖率可能导致写无意义的测试。一般 80% 以上就不错了。

---

## 9. 项目配置：pyproject.toml

在 `pyproject.toml` 中集中配置 pytest，避免每次敲长命令：

```toml
[tool.pytest.ini_options]
# 测试搜索路径
testpaths = ["tests"]
# 自定义标记
markers = [
    "slow: 标记耗时较长的测试",
    "integration: 集成测试",
]
# 命令行默认选项
addopts = "-v --tb=short"
```

配置好之后，直接 `uv run pytest` 就会自动应用这些选项。

---

## 10. 实战：一个完整的测试示例

假设我们在写一个用户管理模块：

```python
# user_manager.py
class UserManager:
    def __init__(self):
        self._users = {}

    def add(self, user_id, name):
        if user_id in self._users:
            raise ValueError(f"用户 {user_id} 已存在")
        self._users[user_id] = {"name": name}
        return self._users[user_id]

    def get(self, user_id):
        if user_id not in self._users:
            raise KeyError(f"用户 {user_id} 不存在")
        return self._users[user_id]

    def delete(self, user_id):
        if user_id not in self._users:
            raise KeyError(f"用户 {user_id} 不存在")
        del self._users[user_id]

    def list_all(self):
        return dict(self._users)
```

```python
# test_user_manager.py
import pytest
from user_manager import UserManager


@pytest.fixture
def manager():
    """每个测试都用一个全新的 UserManager"""
    mgr = UserManager()
    mgr.add(1, "张三")
    mgr.add(2, "李四")
    return mgr


class TestAdd:
    def test_add_new_user(self, manager):
        user = manager.add(3, "王五")
        assert user["name"] == "王五"

    def test_add_duplicate_raises(self, manager):
        with pytest.raises(ValueError, match="已存在"):
            manager.add(1, "重复的张三")


class TestGet:
    def test_get_existing(self, manager):
        user = manager.get(1)
        assert user["name"] == "张三"

    def test_get_nonexistent_raises(self, manager):
        with pytest.raises(KeyError, match="不存在"):
            manager.get(999)


class TestDelete:
    def test_delete_existing(self, manager):
        manager.delete(1)
        assert 1 not in manager.list_all()

    def test_delete_nonexistent_raises(self, manager):
        with pytest.raises(KeyError):
            manager.delete(999)


class TestListAll:
    def test_returns_all_users(self, manager):
        all_users = manager.list_all()
        assert len(all_users) == 2
        assert 1 in all_users
        assert 2 in all_users
```

运行结果：

```
test_user_manager.py::TestAdd::test_add_new_user PASSED
test_user_manager.py::TestAdd::test_add_duplicate_raises PASSED
test_user_manager.py::TestGet::test_get_existing PASSED
test_user_user_manager.py::TestGet::test_get_nonexistent_raises PASSED
test_user_manager.py::TestDelete::test_delete_existing PASSED
test_user_manager.py::TestDelete::test_delete_nonexistent_raises PASSED
test_user_manager.py::TestListAll::test_returns_all_users PASSED
7 passed in 0.02s
```

---

## 本章小结

| 概念                        | 说明                                | 重要程度 |
| --------------------------- | ----------------------------------- | -------- |
| `assert`                    | 断言条件为真，pytest 增强了失败信息 | ⭐⭐⭐      |
| `pytest.raises`             | 测试代码是否抛出了预期的异常        | ⭐⭐⭐      |
| `pytest.approx`             | 浮点数的近似比较                    | ⭐⭐       |
| `@pytest.mark.parametrize`  | 用多组数据测试同一个逻辑            | ⭐⭐⭐      |
| `@pytest.fixture`           | 测试的准备和清理（setup/teardown）  | ⭐⭐⭐      |
| `scope`                     | 控制 fixture 的生命周期             | ⭐⭐       |
| `conftest.py`               | 跨文件共享 fixture                  | ⭐⭐       |
| `skip` / `skipif` / `xfail` | 控制测试的执行行为                  | ⭐⭐       |
| `--cov`                     | 测试覆盖率                          | ⭐        |
| `pyproject.toml`            | 集中配置 pytest                     | ⭐        |

---

## 下一步

恭喜你完成了**进阶篇**！进入 [第 18 章：项目结构](../../03-python-practice/18-project-structure/README.md)，开始实战之旅。
