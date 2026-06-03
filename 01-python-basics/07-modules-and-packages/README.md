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

📖 **详细教程**：[random 标准库教程](./random-stdlib.md) —— 随机数生成、随机选择、权重抽样、种子控制等

### math —— 数学

```python
import math

print(math.pi)         # 3.141592653589793
print(math.sqrt(16))   # 4.0
print(math.ceil(3.2))  # 4（向上取整）
print(math.floor(3.8)) # 3（向下取整）
```

📖 **详细教程**：[math 标准库教程](./math-stdlib.md) —— 取整、幂运算、三角函数、排列组合等

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

📖 **详细教程**：[datetime 标准库教程](./datetime-stdlib.md) —— 日期创建、格式化、解析、时区处理、时间计算等

### pathlib —— 路径操作

```python
from pathlib import Path

current = Path.cwd()
print(f"当前目录: {current}")

config = current / "config" / "settings.json"    # 路径拼接
print(f"配置路径: {config}")
print(f"是否存在: {current.exists()}")
```

📖 **详细教程**：[pathlib 标准库教程](./pathlib-stdlib.md) —— 路径拼接、文件读写、目录遍历、glob 模式匹配等

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

📖 **详细教程**：[json 标准库教程](./json-stdlib.md) —— JSON 读写、序列化陷阱、自定义编解码等

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

## 7. `python -m` 运行模块与包

### 用 `-m` 运行标准库模块

`python -m` 的意思是**把模块当脚本运行**。你已经知道 `python hello.py` 是直接运行一个文件，而 `-m` 是通过**模块名**来运行：

```powershell
# 格式化 JSON（把 stdin 或文件内容格式化输出）
echo '{"name":"小明"}' | python -m json.tool

# 启动一个简易 HTTP 服务器（在当前目录提供文件下载）
python -m http.server 8000

# 运行测试
python -m pytest
```

这些标准库模块本来只能被 `import`，加了 `-m` 就能直接当命令行工具用了。

### `__main__.py` —— 包的入口文件

单文件模块可以用 `if __name__ == "__main__"` 来区分直接运行和被导入。**包**也可以直接运行，秘密就是 `__main__.py`：

```
calculator/
├── __init__.py       # 包标识
├── __main__.py       # python -m calculator 时执行这个文件
├── basic.py
└── advanced.py
```

```python
# calculator/__main__.py
from calculator import add, subtract, power
import sys

if len(sys.argv) < 4:
    print("用法: python -m calculator <操作> <a> <b>")
    print("操作: add / subtract / power")
    sys.exit(1)

operation = sys.argv[1]
a, b = int(sys.argv[2]), int(sys.argv[3])

if operation == "add":
    print(f"{a} + {b} = {add(a, b)}")
elif operation == "subtract":
    print(f"{a} - {b} = {subtract(a, b)}")
elif operation == "power":
    print(f"{a} ^ {b} = {power(a, b)}")
else:
    print(f"未知操作: {operation}")
```

运行方式：

```powershell
# 在 07-modules-and-packages 目录下执行
python -m calculator add 3 5        # 3 + 5 = 8
python -m calculator power 2 10     # 2 ^ 10 = 1024
```

### `-m` 与直接运行的区别

| 方式         | 命令                            | `__name__`   | 模块搜索路径     |
| ------------ | ------------------------------- | ------------ | ---------------- |
| 直接运行文件 | `python calculator/__main__.py` | `"__main__"` | 文件所在目录     |
| 用 `-m` 运行 | `python -m calculator`          | `"__main__"` | **当前工作目录** |

关键区别在于 **模块搜索路径**：

```powershell
# ❌ 直接运行——Python 把 calculator/ 加入搜索路径
#    此时 import basic 可以，但 import calculator 会失败
python calculator/__main__.py

# ✅ 用 -m——Python 把当前目录（07-modules-and-packages/）加入搜索路径
#    import calculator 正常工作，包内的相对导入也正确
python -m calculator
```

> **建议**：运行包时始终使用 `python -m 包名`，不要直接运行包内的文件。

---

## 8. 常见的坑

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

## 9. Python 特殊文件一览

Python 有一系列以双下划线命名（俗称 **dunder**，double underscore）的特殊文件和变量，它们各有约定俗成的用途：

### 模块与包相关

| 名称          | 类型 | 作用                                                             |
| ------------- | ---- | ---------------------------------------------------------------- |
| `__init__.py` | 文件 | 标记目录为 Python 包。可以为空，也可以放包的初始化代码和导入转发 |
| `__main__.py` | 文件 | 包的入口文件。`python -m 包名` 时执行此文件                      |
| `__all__`     | 变量 | 列表，控制 `from xxx import *` 的导出范围                        |
| `__name__`    | 变量 | 模块名。直接运行时为 `"__main__"`，被导入时为模块的完整路径名    |
| `__version__` | 变量 | 版本号约定（如 `"1.0.0"`）。非强制，但几乎所有第三方库都用它     |
| `__file__`    | 变量 | 当前模块文件的绝对路径。调试时常用：`print(__file__)`            |

### 运行时相关

| 名称           | 说明                                                                                                              |
| -------------- | ----------------------------------------------------------------------------------------------------------------- |
| `__pycache__/` | 目录，存放 Python 编译后的字节码文件（`.pyc`）。首次导入时自动生成，加速后续导入。可以安全删除，Python 会重新生成 |
| `__doc__`      | 模块、类、函数的文档字符串（docstring）。`help()` 函数就是读取它                                                  |

### 项目配置相关

这些不是双下划线命名，但同样是 Python 生态中的约定性文件：

| 文件              | 作用                                                                               |
| ----------------- | ---------------------------------------------------------------------------------- |
| `pyproject.toml`  | 项目核心配置文件。定义元数据、依赖、构建系统、工具配置等（现代 Python 项目的标准） |
| `py.typed`        | 空文件，放在包根目录。告诉类型检查器（mypy 等）这个包自带类型注解                  |
| `.python-version` | 固定项目使用的 Python 版本（如 `3.12`）。uv、pyenv 等工具会读取它                  |
| `conftest.py`     | pytest 的共享配置文件。放在项目根目录或测试目录中，定义全局的 fixture              |

### 命名约定

Python 社区有一些广泛遵循的命名约定：

```python
# _ 单下划线开头：内部使用，不建议外部调用（但不会阻止）
def _internal_helper():
    pass

# __ 双下划线开头（不在尾部的）：触发名称改写（name mangling）
class MyClass:
    def __init__(self):
        self.__private = 42    # 实际名称变为 _MyClass__private

# __xx__ 双下划线包围：Python 保留的特殊方法/属性（魔术方法）
def __init__(self):     # 构造函数
def __str__(self):      # print() 时调用
def __repr__(self):     # 调试时显示
def __len__(self):      # len() 时调用
```

> **规则**：不要自己发明 `__xx__` 形式的名称，这是 Python 留给自己用的。

---

## 本章小结

| 概念                        | 说明                                     |
| --------------------------- | ---------------------------------------- |
| `import 模块`               | 导入整个模块                             |
| `from 模块 import 名称`     | 导入特定功能                             |
| `as`                        | 重命名                                   |
| `if __name__ == "__main__"` | 区分直接运行和被导入                     |
| 包                          | 文件夹 + `__init__.py`                   |
| `__all__`                   | 控制 `import *` 的导出范围               |
| 绝对导入                    | `from pkg.module import fn`（推荐）      |
| 相对导入                    | `from .module import fn`                 |
| `python -m 包名`            | 以模块方式运行，执行包内的 `__main__.py` |
| `__main__.py`               | 包的入口文件                             |
| `__pycache__/`              | 字节码缓存目录                           |
| `__version__`               | 版本号约定                               |
| `__file__`                  | 模块文件路径                             |
| `__doc__`                   | 文档字符串                               |
| `_` / `__xx__`              | 命名约定（内部使用 / 魔术方法）          |

---

## 下一步

进入 [第 8 章：文件 I/O](../08-file-io/README.md)。
