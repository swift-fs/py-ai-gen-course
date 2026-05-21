# 第 12 章：生成器与迭代器

> **学习目标**：理解迭代器协议，掌握 yield 和生成器，学会用 itertools 处理序列数据。

---

## 1. 可迭代对象和迭代器

### 可迭代对象（Iterable）

能用 `for` 循环遍历的对象：列表、字符串、字典、集合、range……

### 迭代器（Iterator）

实现了 `__iter__()` 和 `__next__()` 方法的对象：

```python
# 手动使用迭代器
numbers = [1, 2, 3]
it = iter(numbers)         # 获取迭代器
print(next(it))            # 1
print(next(it))            # 2
print(next(it))            # 3
# print(next(it))          # StopIteration（没有更多元素了）
```

> `for` 循环的本质：先调用 `iter()` 获取迭代器，然后反复调用 `next()` 直到 `StopIteration`。

---

## 2. 生成器函数（Generator）

用 `yield` 关键字的函数就是生成器。调用时不会立即执行，而是返回一个生成器对象：

```python
def count_up(max_value):
    """生成从 1 到 max_value 的数字"""
    current = 1
    while current <= max_value:
        yield current       # 暂停，返回 current
        current += 1

gen = count_up(3)
print(type(gen))            # <class 'generator'>

print(next(gen))            # 1
print(next(gen))            # 2
print(next(gen))            # 3
# print(next(gen))          # StopIteration

# 更常见：用 for 遍历
for num in count_up(5):
    print(num, end=" ")     # 1 2 3 4 5
```

### yield vs return

| 特性 | `return` | `yield` |
|------|---------|---------|
| 执行 | 函数结束 | 暂停，下次接着执行 |
| 返回值 | 单个值 | 逐个产生值（惰性） |
| 内存 | 一次加载全部 | 只在需要时产生 |

---

## 3. 生成器的优势——省内存

```python
# ❌ 一次创建100万个数字，占大量内存
# numbers = [x ** 2 for x in range(1_000_000)]

# ✅ 生成器：按需产生，几乎不占内存
def squares(n):
    for i in range(n):
        yield i ** 2

# 只在需要时计算下一个值
for s in squares(10):
    print(s, end=" ")    # 0 1 4 9 16 25 36 49 64 81
```

### 生成器表达式

```python
# 类似列表推导式，但用圆括号
squares = (x ** 2 for x in range(10))
print(type(squares))    # <class 'generator'>

# 求前 100 万个数的平方和（不需要创建列表）
total = sum(x ** 2 for x in range(1_000_000))
```

---

## 4. 实用生成器示例

### 读取大文件

```python
def read_large_file(file_path):
    """逐行读取大文件，不会一次性加载到内存"""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# for line in read_large_file("huge_file.txt"):
#     process(line)
```

### 斐波那契数列

```python
def fibonacci():
    """无限斐波那契数列生成器"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 取前 10 个
fib = fibonacci()
first_ten = [next(fib) for _ in range(10)]
print(first_ten)    # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## 5. itertools 常用工具

```python
import itertools

# chain —— 连接多个可迭代对象
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print(combined)    # [1, 2, 3, 4, 5]

# combinations —— 组合（不考虑顺序）
for combo in itertools.combinations("ABC", 2):
    print(combo)
# ('A', 'B'), ('A', 'C'), ('B', 'C')

# permutations —— 排列（考虑顺序）
for perm in itertools.permutations("AB", 2):
    print(perm)
# ('A', 'B'), ('B', 'A')

# groupby —— 分组
students = [
    {"name": "小明", "grade": "A"},
    {"name": "小红", "grade": "B"},
    {"name": "小刚", "grade": "A"},
]
students.sort(key=lambda s: s["grade"])    # groupby 前必须排序！
for grade, group in itertools.groupby(students, key=lambda s: s["grade"]):
    names = [s["name"] for s in group]
    print(f"{grade}: {names}")

# count —— 无限计数器
for i in itertools.count(start=1, step=2):
    if i > 10:
        break
    print(i)    # 1, 3, 5, 7, 9

# islice —— 切片（对任何可迭代对象）
first_five = list(itertools.islice(range(100), 5))
print(first_five)    # [0, 1, 2, 3, 4]
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| 迭代器 | 实现 `__iter__` + `__next__` |
| `iter()` | 获取迭代器 |
| `next()` | 获取下一个值 |
| `yield` | 暂停函数，返回值 |
| 生成器 | 含 yield 的函数，惰性求值 |
| 生成器表达式 | `(expr for x in iterable)` |
| `itertools` | 迭代器工具库 |

---

## 下一步

进入 [第 13 章：类型注解](../13-type-annotations/README.md)。
