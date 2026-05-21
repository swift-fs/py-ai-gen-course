# 第 15 章：标准库深入

> **学习目标**：掌握常用标准库的高级用法——正则表达式、collections、functools、pathlib 进阶。

---

## 1. re —— 正则表达式

正则表达式用于在字符串中**查找、替换、验证**特定模式：

### 基本匹配

```python
import re

text = "联系方式：电话138-1234-5678，邮箱test@example.com"

# findall —— 找到所有匹配
phones = re.findall(r"\d{3}-\d{4}-\d{4}", text)
print(phones)    # ['138-1234-5678']

emails = re.findall(r"[\w.]+@[\w]+\.[\w]+", text)
print(emails)    # ['test@example.com']
```

### 替换

```python
# sub —— 替换匹配内容
hidden = re.sub(r"\d{4}", "****", "138-1234-5678")
print(hidden)    # 138-****-****

# 用函数动态替换
def upper_match(m):
    return m.group(0).upper()

result = re.sub(r"hello", upper_match, "say hello world")
print(result)    # say HELLO world
```

### 验证

```python
# match —— 从头匹配
email = "test@example.com"
pattern = r"^[\w.]+@[\w]+\.[\w]+$"
if re.match(pattern, email):
    print("邮箱格式正确")

# search —— 在任意位置搜索
text = "我的成绩是95分"
m = re.search(r"(\d+)分", text)
if m:
    print(f"分数: {m.group(1)}")    # 分数: 95
```

### 常用正则模式

| 模式 | 含义 | 示例 |
|------|------|------|
| `\d` | 数字 | `\d{3}` |
| `\w` | 字母/数字/下划线 | `\w+` |
| `\s` | 空白字符 | `\s+` |
| `.` | 任意字符 | `a.c` |
| `*` | 0 次或多次 | `ab*c` |
| `+` | 1 次或多次 | `ab+c` |
| `?` | 0 次或 1 次 | `colou?r` |
| `^` / `$` | 开头 / 结尾 | `^hello$` |
| `()` | 捕获组 | `(\d+)-(\d+)` |
| `[]` | 字符集 | `[aeiou]` |

---

## 2. collections —— 特殊容器

### Counter —— 计数器

```python
from collections import Counter

words = ["苹果", "香蕉", "苹果", "橙子", "香蕉", "苹果"]
count = Counter(words)
print(count)                 # Counter({'苹果': 3, '香蕉': 2, '橙子': 1})
print(count.most_common(2))  # [('苹果', 3), ('香蕉', 2)]
print(count["苹果"])          # 3
print(count["葡萄"])          # 0（不存在返回0，不报错）

# 计数器运算
c1 = Counter("aabbcc")
c2 = Counter("aabbd")
print(c1 + c2)    # 加法
print(c1 - c2)    # 减法（只保留正数）
```

### defaultdict —— 带默认值的字典

```python
from collections import defaultdict

# 普通字典的问题
# d = {}
# d["key"].append(1)    # ❌ KeyError!

# defaultdict 自动创建默认值
grades = defaultdict(list)    # 不存在的键返回空列表
grades["小明"].append(95)
grades["小明"].append(88)
grades["小红"].append(92)
print(dict(grades))    # {'小明': [95, 88], '小红': [92]}

# 计数
counter = defaultdict(int)    # 默认值是 0
for char in "hello":
    counter[char] += 1
print(dict(counter))    # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

### namedtuple —— 命名元组

```python
from collections import namedtuple

# 创建命名元组类
Point = namedtuple("Point", ["x", "y"])
Student = namedtuple("Student", ["name", "age", "score"])

# 使用
p = Point(3, 4)
print(p.x, p.y)          # 3 4（用名字访问，比索引更清晰）
print(p[0], p[1])        # 3 4（也支持索引）

s = Student("小明", 18, 88)
print(f"{s.name}: {s.score}分")

# 转换为字典
print(s._asdict())        # {'name': '小明', 'age': 18, 'score': 88}
```

---

## 3. functools —— 函数工具

### reduce —— 累积计算

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, numbers)
print(total)    # 15

# 等价于：((((1+2)+3)+4)+5)

# 带初始值
total = reduce(lambda a, b: a + b, numbers, 100)
print(total)    # 115
```

### partial —— 偏函数（固定部分参数）

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# 固定 exponent 参数
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))    # 25
print(cube(3))      # 27
```

### lru_cache —— 缓存

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))    # 瞬间计算（缓存避免重复计算）
print(fibonacci.cache_info())    # 查看缓存统计
```

---

## 4. pathlib 进阶

```python
from pathlib import Path

# 遍历目录
for item in Path(".").iterdir():
    if item.is_file():
        print(f"文件: {item.name}")
    elif item.is_dir():
        print(f"目录: {item.name}/")

# 递归查找所有 Python 文件
for py_file in Path(".").rglob("*.py"):
    print(py_file)

# 文件操作
p = Path("data")
p.mkdir(exist_ok=True)                 # 创建目录
(p / "test.txt").write_text("hello")   # 写文件
(p / "test.txt").unlink()              # 删除文件
p.rmdir()                              # 删除空目录

# 路径拼接和解析
p = Path("/home/user/docs/report.txt")
print(p.parent)     # /home/user/docs
print(p.stem)       # report（不带后缀的文件名）
print(p.suffix)     # .txt
print(p.name)       # report.txt
```

---

## 本章小结

| 库 | 工具 | 用途 |
|---|------|------|
| `re` | `findall/sub/match/search` | 正则表达式 |
| `collections` | `Counter` | 计数 |
| `collections` | `defaultdict` | 带默认值的字典 |
| `collections` | `namedtuple` | 命名元组 |
| `functools` | `reduce` | 累积计算 |
| `functools` | `partial` | 固定部分参数 |
| `functools` | `lru_cache` | 自动缓存 |
| `pathlib` | `rglob/iterdir` | 文件查找遍历 |

---

## 下一步

进入 [第 16 章：设计模式](../16-design-patterns/README.md)。
