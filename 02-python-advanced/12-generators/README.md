# 第 12 章：生成器与迭代器

> **学习目标**：理解迭代器协议，掌握 yield 和生成器，学会用 itertools 处理序列数据。

---

## 1. 从 for 循环说起——可迭代对象

你已经用过很多次 `for` 循环了：

```python
for num in [1, 2, 3]:
    print(num)

for char in "Hello":
    print(char)

for key in {"name": "小明", "age": 18}:
    print(key)
```

列表、字符串、字典、集合、`range()`……这些能用 `for` 循环遍历的对象，有一个共同的名字：**可迭代对象（Iterable）**。

> **类比**：可迭代对象就像一盒巧克力，你可以一颗一颗地拿出来，但你不知道里面是怎么排列的。

---

## 2. 迭代器——for 循环的幕后英雄

`for` 循环背后到底发生了什么？答案是**迭代器（Iterator）**。

### 2.1 手动使用迭代器

每个可迭代对象都可以通过 `iter()` 转换成一个迭代器，然后用 `next()` 逐个取值：

```python
numbers = [1, 2, 3]
it = iter(numbers)          # 获取迭代器

print(next(it))             # 1
print(next(it))             # 2
print(next(it))             # 3
# print(next(it))           # 报错！StopIteration（没有更多元素了）
```

### 2.2 for 循环的本质

`for` 循环其实就是在帮你做这件事：

```python
# for num in [1, 2, 3]:
#     print(num)
#
# 等价于：
it = iter([1, 2, 3])
while True:
    try:
        num = next(it)
        print(num)
    except StopIteration:
        break
```

> **理解要点**：迭代器就像一个游标，每次 `next()` 向前移动一步，走到头就抛出 `StopIteration`。`for` 循环会自动帮你处理这个异常。

### 2.3 迭代器只能用一次

这是一个容易踩的坑：

```python
numbers = [1, 2, 3]
it = iter(numbers)

print(list(it))             # [1, 2, 3] —— 全部取出来了
print(list(it))             # [] —— 迭代器已经用完了！

# 但原始列表不受影响
print(numbers)              # [1, 2, 3]
```

> **记住**：迭代器是一次性的，用完就空了。如果需要重新遍历，就再调用 `iter()` 创建一个新的迭代器。

---

## 3. 生成器函数——用 yield 暂停函数

### 3.1 什么是生成器？

普通函数用 `return` 返回结果，函数就结束了。**生成器函数**用 `yield` 返回结果，但函数不会结束——它会**暂停**，等你下次要值的时候再继续：

```python
def count_up(max_value):
    """生成从 1 到 max_value 的数字"""
    current = 1
    while current <= max_value:
        yield current       # 暂停在这里，把 current 交出去
        current += 1        # 下次从这里继续执行

# 调用生成器函数，不会执行函数体，而是返回一个生成器对象
gen = count_up(3)
print(type(gen))            # <class 'generator'>

print(next(gen))            # 1
print(next(gen))            # 2
print(next(gen))            # 3
# print(next(gen))          # StopIteration
```

> **类比**：想象一个自动售货机。你投一次币（调用 `next()`），它吐出一瓶饮料（`yield` 一个值），然后等你再投币。直到饮料卖完，它就告诉你"售罄"（`StopIteration`）。

### 3.2 yield vs return

| 特性 | `return` | `yield` |
|------|---------|---------|
| 执行 | 函数**结束** | 函数**暂停**，下次接着执行 |
| 返回值 | 返回一个值 | 逐个产生多个值 |
| 调用方式 | 直接得到结果 | 返回生成器对象，按需取值 |
| 内存 | 一次加载全部数据 | 只在需要时产生，极其省内存 |

### 3.3 用 for 循环遍历生成器

在实际开发中，我们很少手动调用 `next()`，而是直接用 `for` 循环：

```python
for num in count_up(5):
    print(num, end=" ")     # 1 2 3 4 5
```

生成器也是一种迭代器，所以 `for` 循环可以完美配合。

---

## 4. 生成器的超能力——省内存

### 4.1 问题：如果我们要处理 100 万个数据

```python
# ❌ 一次创建 100 万个数字的列表，占大量内存
big_list = [x ** 2 for x in range(1_000_000)]
# 内存占用约 40MB+

# ✅ 生成器：按需产生，几乎不占内存
big_gen = (x ** 2 for x in range(1_000_000))
# 内存占用几乎为 0
```

### 4.2 生成器表达式

和列表推导式很像，但用**圆括号**而不是方括号：

```python
# 列表推导式 —— 一次性创建所有数据
squares_list = [x ** 2 for x in range(5)]
print(type(squares_list))   # <class 'list'>
print(squares_list)         # [0, 1, 4, 9, 16]

# 生成器表达式 —— 按需产生数据
squares_gen = (x ** 2 for x in range(5))
print(type(squares_gen))    # <class 'generator'>
print(list(squares_gen))    # [0, 1, 4, 9, 16]（用 list() 一次性取出）

# 常用场景：配合 sum()、max() 等函数
total = sum(x ** 2 for x in range(10))
print(total)                # 285
```

> **什么时候用生成器表达式？** 当你不需要把所有结果同时存在内存里，只是想遍历或聚合时，就用它。比如 `sum()`、`max()`、`any()` 等场景。

---

## 5. 实用生成器示例

### 5.1 读取大文件

当文件很大（比如几个 GB）时，一次性读取会撑爆内存。生成器可以逐行处理：

```python
def read_large_file(file_path):
    """逐行读取大文件，不会一次性加载到内存"""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# 每次只有一行在内存中
# for line in read_large_file("huge_file.txt"):
#     process(line)
```

### 5.2 斐波那契数列

斐波那契数列是无限的（0, 1, 1, 2, 3, 5, 8, 13...），用列表无法表示"无限"。但生成器可以：

```python
def fibonacci():
    """无限斐波那契数列生成器"""
    a, b = 0, 1
    while True:             # 无限循环！但不会卡住
        yield a
        a, b = b, a + b

# 按需取值：要多少取多少
fib = fibonacci()
first_ten = [next(fib) for _ in range(10)]
print(first_ten)            # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

> **为什么不会卡住？** 因为 `yield` 会暂停函数。每次 `next()` 只执行到 `yield` 就停了，不会一直循环。

### 5.3 数据管道——生成器组合

生成器可以像流水线一样串起来，每一步只处理当前数据：

```python
def get_numbers():
    """产生 1 到 10 的数字"""
    for i in range(1, 11):
        yield i

def filter_even(numbers):
    """只保留偶数"""
    for n in numbers:
        if n % 2 == 0:
            yield n

def square(numbers):
    """对每个数求平方"""
    for n in numbers:
        yield n ** 2

# 管道：数字 → 过滤偶数 → 求平方
pipeline = square(filter_even(get_numbers()))
print(list(pipeline))       # [4, 16, 36, 64, 100]
```

这种模式在处理大数据时非常有用——每个环节都不需要把所有数据存进内存。

---

## 6. itertools——迭代器工具箱

Python 内置的 `itertools` 模块提供了很多现成的迭代器工具，不用自己写。

### 6.1 chain —— 连接多个序列

```python
import itertools

# 把多个列表拼接成一个迭代器
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print(combined)             # [1, 2, 3, 4, 5]
```

### 6.2 combinations —— 组合（不考虑顺序）

```python
# 从 "ABC" 中选 2 个的所有组合
combos = list(itertools.combinations("ABC", 2))
print(combos)
# [('A', 'B'), ('A', 'C'), ('B', 'C')]
```

### 6.3 permutations —— 排列（考虑顺序）

```python
# 从 "AB" 中选 2 个的所有排列
perms = list(itertools.permutations("AB", 2))
print(perms)
# ('A', 'B'), ('B', 'A')
```

### 6.4 groupby —— 分组

```python
students = [
    {"name": "小明", "grade": "A"},
    {"name": "小红", "grade": "B"},
    {"name": "小刚", "grade": "A"},
]

# ⚠️ groupby 前必须排序！它只合并相邻的相同组
students.sort(key=lambda s: s["grade"])

for grade, group in itertools.groupby(students, key=lambda s: s["grade"]):
    names = [s["name"] for s in group]
    print(f"  {grade}组: {names}")
# A组: ['小明', '小刚']
# B组: ['小红']
```

### 6.5 count —— 无限计数器

```python
# 从 1 开始，每次加 2
for i in itertools.count(start=1, step=2):
    if i > 10:
        break
    print(i, end=" ")       # 1 3 5 7 9
```

### 6.6 islice —— 对迭代器切片

普通切片 `list[0:5]` 只能用于列表。`islice` 可以对任何迭代器切片：

```python
# 只取前 5 个
first_five = list(itertools.islice(range(100), 5))
print(first_five)           # [0, 1, 2, 3, 4]
```

---

## 7. 常见错误与注意事项

### 错误 1：迭代器只能用一次

```python
gen = (x for x in range(3))
print(list(gen))            # [0, 1, 2]
print(list(gen))            # [] ← 空了！生成器是一次性的
```

### 错误 2：groupby 前忘记排序

```python
data = [("A", 1), ("B", 2), ("A", 3)]
# 忘记排序就 groupby，"A" 会被分成两组！
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A [('A', 1)]
# B [('B', 2)]
# A [('A', 3)]  ← 又出现了一个 A 组！
```

### 错误 3：在生成器上使用 len()

```python
gen = (x for x in range(5))
# len(gen)                  # TypeError! 生成器没有长度
print(list(gen))            # 需要先转换成列表
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| 可迭代对象（Iterable） | 能用 `for` 遍历的对象（列表、字符串等） |
| 迭代器（Iterator） | 用 `iter()` 获取，用 `next()` 取值 |
| `yield` | 暂停函数，交出一个值，下次继续 |
| 生成器函数 | 含 `yield` 的函数，返回生成器对象 |
| 生成器表达式 | `(expr for x in iterable)`，省内存 |
| `itertools` | 迭代器工具箱（chain、groupby 等） |

**核心思想**：生成器让你**按需产生数据**，而不是一次性创建所有数据。这在处理大数据、无限序列、数据管道时特别有用。

---

## 下一步

进入 [第 13 章：类型注解](../13-type-annotations/README.md)。
