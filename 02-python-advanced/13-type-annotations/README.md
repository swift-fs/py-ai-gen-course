# 第 13 章：类型注解

> **学习目标**：学会使用类型注解提高代码可读性，了解 mypy 静态类型检查。

---

## 1. 基本类型注解

```python
# 变量注解
name: str = "小明"
age: int = 18
height: float = 1.75
is_student: bool = True

# Python 不会强制检查类型，注解只是"提示"
name = 123    # 不会报错！类型注解不影响运行
```

### 函数注解

```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"你好，{name}"

# 没有返回值的函数用 None
def print_hello() -> None:
    print("Hello")
```

---

## 2. 容器类型

```python
from typing import List, Dict, Set, Tuple, Optional

# 列表、字典、集合、元组
names: List[str] = ["小明", "小红"]
scores: Dict[str, int] = {"小明": 88, "小红": 95}
unique: Set[int] = {1, 2, 3}
point: Tuple[float, float] = (3.0, 4.0)

# Python 3.9+ 可以直接用内置类型
names: list[str] = ["小明", "小红"]
scores: dict[str, int] = {"小明": 88}
```

### Optional —— 可能为 None

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    """可能返回字符串，也可能返回 None"""
    if user_id == 1:
        return "小明"
    return None

result = find_user(1)    # 类型检查器知道 result 可能是 str 或 None
```

### Union —— 多种类型之一

```python
from typing import Union

def process(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return str(value)
    return value

# Python 3.10+ 可以用 | 语法
def process(value: int | str) -> str:
    if isinstance(value, int):
        return str(value)
    return value
```

---

## 3. Callable 和 TypeAlias

```python
from typing import Callable

# Callable 表示"函数类型"
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

double = lambda x: x * 2
print(apply(double, 5))    # 10

# TypeAlias —— 类型别名
from typing import TypeAlias
UserId: TypeAlias = int
UserName: TypeAlias = str

def get_user(uid: UserId) -> UserName:
    return "小明"
```

---

## 4. 用 dataclass 配合类型注解

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    scores: list[float]    # Python 3.9+
    email: str | None = None    # 可选字段

    def average(self) -> float:
        return sum(self.scores) / len(self.scores)

s = Student("小明", 18, [88.0, 92.0, 85.0])
print(f"{s.name}: {s.average():.1f}")
```

---

## 5. mypy 静态类型检查

mypy 是一个工具，在**运行前**检查类型错误：

```powershell
uv add --dev mypy
uv run mypy your_script.py
```

```python
# your_script.py
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)       # ✅
add("a", "b")   # ❌ mypy 会报错：Argument 1 to "add" has incompatible type "str"
```

> 类型注解 + mypy = 在写代码时就能发现潜在错误，而不是运行时才崩溃。

---

## 本章小结

| 注解 | 说明 | 示例 |
|------|------|------|
| `int`, `str`, `float`, `bool` | 基本类型 | `age: int` |
| `list[str]` | 列表 | `names: list[str]` |
| `dict[str, int]` | 字典 | `scores: dict[str, int]` |
| `Optional[str]` | 可能为 None | `-> Optional[str]` |
| `Union[int, str]` | 多种类型 | `int \| str` (3.10+) |
| `Callable` | 函数类型 | `func: Callable` |
| `mypy` | 静态类型检查工具 | `mypy script.py` |

---

## 下一步

进入 [第 14 章：异步编程](../14-async/README.md)。
