# 第 7 章：模块与包

> **学习目标**：学会组织代码——使用标准库模块、创建自己的模块和包、理解导入机制和常见陷阱。

---

## 1. 什么是模块？

**模块**就是一个 `.py` 文件。你写的每个 Python 文件都可以被其他文件导入使用。

Python 自带了大量**标准库模块**，不需要安装就能用。

---

## 2. import 的几种方式

### 导入整个模块

```python
import random
print(random.randint(1, 10))    # 模块名.函数名
```

### 导入特定功能

```python
from random import randint, choice
print(randint(1, 10))           # 直接用函数名
```

### 导入并重命名

```python
import datetime as dt
print(dt.datetime.now())

from collections import Counter as C
print(C(["a", "b", "a"]))
```

### 导入所有（不推荐）

```python
from random import *
# 会导入所有公开名称，容易命名冲突
```

> **最佳实践**：用 `import 模块名` 或 `from 模块名 import 具体名称`。避免 `import *`。

---

## 3. 常用标准库速览

### random —— 随机

```python
import random

print(random.randint(1, 10))      # 随机整数
print(random.choice(["A", "B"]))  # 随机选择

items = [1, 2, 3, 4, 5]
random.shuffle(items)             # 打乱顺序
print(items)
```

### math —— 数学

```python
import math

print(math.pi)         # 3.141592653589793
print(math.sqrt(16))   # 4.0
print(math.ceil(3.2))  # 4（向上取整）
print(math.floor(3.8)) # 3（向下取整）
```

### datetime —— 日期时间

```python
from datetime import datetime, timedelta

now = datetime.now()
print(now)
print(now.strftime("%Y-%m-%d %H:%M"))    # 格式化

tomorrow = now + timedelta(days=1)
print(f"明天: {tomorrow.strftime('%Y-%m-%d')}")

# 字符串转日期
date = datetime.strptime("2024-06-01", "%Y-%m-%d")
```

### pathlib —— 路径操作

```python
from pathlib import Path

current = Path.cwd()
print(f"当前目录: {current}")

config = current / "config" / "settings.json"    # 路径拼接
print(f"配置路径: {config}")
print(f"是否存在: {current.exists()}")
```

### json —— JSON 数据

```python
import json

# Python 对象 → JSON 字符串
data = {"name": "小明", "scores": [95, 88]}
text = json.dumps(data, ensure_ascii=False, indent=2)
print(text)

# JSON 字符串 → Python 对象
parsed = json.loads(text)
print(parsed["name"])
```

---

## 4. 创建自己的模块

任何 `.py` 文件都是一个模块：

```python
# my_tools.py
def add(a, b):
    """加法"""
    return a + b

def greet(name):
    """问候"""
    return f"你好，{name}！"
```

```python
# main.py（和 my_tools.py 同目录）
from my_tools import add, greet

print(add(3, 5))      # 8
print(greet("小明"))   # 你好，小明！
```

### `if __name__ == "__main__"`

```python
# my_tools.py
def add(a, b):
    return a + b

# 直接运行时执行测试，被 import 时不执行
if __name__ == "__main__":
    print("测试:", add(3, 5))    # python my_tools.py 才会输出
```

**原理**：
- 直接运行文件 → `__name__` 是 `"__main__"`
- 被 import 时 → `__name__` 是模块名（如 `"my_tools"`）

---

## 5. 创建包（Package）

**包**就是一个文件夹，里面放多个模块。

```
my_project/
├── main.py
└── calculator/
    ├── __init__.py      # 包标识（可以是空文件）
    ├── basic.py
    └── advanced.py
```

### __init__.py

告诉 Python 这个文件夹是一个包。还可以控制导入行为：

```python
# calculator/__init__.py
from .basic import add, subtract     # 简化导入路径
```

### 模块文件

```python
# calculator/basic.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

```python
# calculator/advanced.py
def power(base, exp):
    return base ** exp
```

### 使用包

```python
# main.py

# 方式 1：完整路径
import calculator.basic
print(calculator.basic.add(3, 5))

# 方式 2：从模块导入
from calculator.basic import add
print(add(3, 5))

# 方式 3：如果 __init__.py 做了转发
from calculator import add
print(add(3, 5))
```

### __all__ 控制导出

```python
# calculator/basic.py
__all__ = ["add", "subtract"]    # import * 只导出这些

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def _internal():    # _ 开头不会被 import * 导入
    pass
```

---

## 6. 相对导入和绝对导入

```python
# 在 calculator/advanced.py 中引用 basic.py

# 绝对导入（推荐）
from calculator.basic import add

# 相对导入
from .basic import add       # . 表示当前包
from ..other import func     # .. 表示上一级包
```

> **建议**：优先用绝对导入，更清晰、更不容易出错。

---

## 7. 常见的坑

### 循环导入

```python
# a.py
from b import hello_b    # ❌ a 导入 b

# b.py
from a import hello_a    # ❌ b 又导入 a → 循环报错
```

**解决方法**：提取公共代码到第三个模块，或者延迟导入（在函数内部 import）。

### 文件名和标准库冲突

```python
# 如果你创建了 random.py
import random    # ❌ 导入的是你自己的文件！
```

**解决**：文件名不要和标准库重名。

### 模块只加载一次

```python
import config    # 第一次：执行 config.py 中的代码
import config    # 第二次：不再执行（Python 缓存了模块）
```

修改模块文件后需要**重启 Python** 才能生效。

### 运行目录

导入模块时，Python 从当前目录开始搜索。确保在**项目根目录**运行程序：

```
cd my_project
python main.py
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| `import 模块` | 导入整个模块 |
| `from 模块 import 名称` | 导入特定功能 |
| `as` | 重命名 |
| `if __name__ == "__main__"` | 区分直接运行和被导入 |
| 包 | 文件夹 + `__init__.py` |
| `__all__` | 控制 `import *` 的导出范围 |
| 绝对导入 | `from pkg.module import fn`（推荐） |
| 相对导入 | `from .module import fn` |

---

## 下一步

进入 [第 8 章：文件 I/O](../08-file-io/README.md)。
