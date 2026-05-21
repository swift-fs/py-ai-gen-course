# 第 6 章：函数

> **学习目标**：全面掌握函数——定义、参数、返回值、作用域、lambda、递归、高阶函数。函数是代码复用的基石。

---

## 1. 定义和调用函数

### 基本语法

```python
def greet():
    """打招呼函数"""    # 文档字符串（docstring），说明函数用途
    print("你好！")

greet()    # 调用函数：函数名()
```

### 带参数

```python
def greet(name):
    print(f"你好，{name}！")

greet("小明")    # 你好，小明！
greet("小红")    # 你好，小红！
```

### 带返回值

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)    # 8
```

> `return` 的作用：把结果返回给调用者。函数执行到 `return` 就立即结束。

### 返回多个值

```python
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder    # 返回一个元组

q, r = divide(17, 5)
print(f"商: {q}, 余: {r}")    # 商: 3, 余: 2
```

---

## 2. 参数详解

### 位置参数 vs 关键字参数

```python
def describe_pet(name, animal):
    print(f"我有一只{animal}，叫{name}")

# 位置参数：按顺序传
describe_pet("旺财", "狗")       # 我有一只狗，叫旺财

# 关键字参数：按名字传（顺序无关）
describe_pet(animal="猫", name="小花")  # 我有一只猫，叫小花

# 混合使用：位置参数必须在前
describe_pet("大黄", animal="狗")  # ✅ 正确
# describe_pet(animal="狗", "大黄")  # ❌ 位置参数不能在关键字参数后面
```

### 默认参数

```python
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("小明")              # 你好，小明！（使用默认值）
greet("小明", "早上好")    # 早上好，小明！（覆盖默认值）
```

⚠️ **默认参数陷阱**：不要用可变对象（列表、字典）作为默认值！

```python
# ❌ 错误：默认列表在多次调用间共享
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['a', 'b']（不是 ['b']！上次的列表还在）

# ✅ 正确：用 None 作为默认值
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### *args —— 收集多余的位置参数

```python
def add_all(*args):
    """可以传入任意数量的参数"""
    print(f"收到参数: {args}（类型: {type(args).__name__}）")
    return sum(args)

print(add_all(1, 2, 3))        # 6
print(add_all(1, 2, 3, 4, 5))  # 15
```

> `*args` 把多余的位置参数收集成一个**元组**。

### **kwargs —— 收集多余的关键字参数

```python
def print_info(**kwargs):
    """可以传入任意数量的关键字参数"""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="小明", age=18, city="北京")
#   name: 小明
#   age: 18
#   city: 北京
```

> `**kwargs` 把多余的关键字参数收集成一个**字典**。

### 组合使用

```python
def func(pos1, pos2, *args, key1="默认", **kwargs):
    """
    参数顺序规则：
    1. 位置参数（必须传）
    2. *args（收集多余位置参数）
    3. 关键字参数（有默认值）
    4. **kwargs（收集多余关键字参数）
    """
    print(f"位置: {pos1}, {pos2}")
    print(f"args: {args}")
    print(f"key1: {key1}")
    print(f"kwargs: {kwargs}")

func("a", "b", "c", "d", key1="覆盖", extra="更多")
```

### 解包参数

```python
def add(a, b, c):
    return a + b + c

# 用 * 把列表/元组解包成位置参数
values = [1, 2, 3]
print(add(*values))    # 6

# 用 ** 把字典解包成关键字参数
params = {"a": 1, "b": 2, "c": 3}
print(add(**params))   # 6
```

---

## 3. 作用域

作用域决定了变量在哪里可以被访问。

```python
message = "全局变量"

def my_function():
    message = "局部变量"     # 这是局部变量，和外部的 message 无关
    print(message)           # 局部变量

my_function()
print(message)               # 全局变量（外部的没被改变）
```

### global 关键字

```python
counter = 0

def increment():
    global counter    # 声明使用全局变量
    counter += 1

increment()
print(counter)    # 1
```

> ⚠️ 尽量少用 `global`。函数应该通过参数接收数据、通过返回值输出结果，而不是直接修改全局变量。

### LEGB 规则

Python 查找变量的顺序：**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)      # local
    inner()

outer()
```

---

## 4. lambda 匿名函数

`lambda` 是一种创建简短匿名函数的方式：

```python
# 语法：lambda 参数: 表达式
square = lambda x: x ** 2
print(square(5))    # 25

# 等价于
def square(x):
    return x ** 2
```

### lambda 的常见用途

```python
# 配合 sorted() 排序
students = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]
by_score = sorted(students, key=lambda s: s["score"])
print([s["name"] for s in by_score])    # ['小刚', '小明', '小红']

# 配合 map() —— 对每个元素应用函数
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)    # [2, 4, 6, 8, 10]

# 配合 filter() —— 过滤元素
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)    # [2, 4]
```

> 建议：简单的逻辑用 lambda，复杂逻辑还是用 `def` 定义正常函数，更可读。

---

## 5. 递归

**递归**是函数调用自身的技巧。每个递归需要两个要素：
1. **终止条件**（什么时候停下来）
2. **递归调用**（问题规模缩小）

### 阶乘

```python
def factorial(n):
    if n <= 1:         # 终止条件
        return 1
    return n * factorial(n - 1)    # 递归调用

print(factorial(5))    # 120（5×4×3×2×1）
```

### 斐波那契数列

```python
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(10):
    print(fibonacci(i), end=" ")    # 0 1 1 2 3 5 8 13 21 34
```

---

## 6. 高阶函数

**高阶函数**：接收函数作为参数，或者返回函数的函数。

### 函数作为参数

```python
def apply(func, value):
    """把 func 应用到 value 上"""
    return func(value)

print(apply(lambda x: x * 2, 5))      # 10
print(apply(lambda x: x.upper(), "hello"))  # HELLO
```

### map() —— 映射

```python
numbers = [1, 2, 3, 4, 5]

# 对每个元素应用函数
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)    # [2, 4, 6, 8, 10]

# 多个列表同时 map
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(sums)    # [11, 22, 33]
```

### filter() —— 过滤

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)    # [2, 4, 6, 8, 10]
```

### sorted() —— 排序

```python
words = ["banana", "apple", "cherry"]
print(sorted(words))                      # ['apple', 'banana', 'cherry']
print(sorted(words, key=len))             # ['apple', 'banana', 'cherry']（按长度）
print(sorted(words, key=len, reverse=True))  # ['banana', 'cherry', 'apple']
```

---

## 7. 常用内置函数速查

| 函数 | 作用 | 示例 |
|------|------|------|
| `len()` | 长度 | `len([1,2,3])` → 3 |
| `sum()` | 求和 | `sum([1,2,3])` → 6 |
| `max()` | 最大值 | `max(1,2,3)` → 3 |
| `min()` | 最小值 | `min(1,2,3)` → 1 |
| `abs()` | 绝对值 | `abs(-5)` → 5 |
| `round()` | 四舍五入 | `round(3.14, 1)` → 3.1 |
| `sorted()` | 排序 | `sorted([3,1,2])` → [1,2,3] |
| `reversed()` | 反转 | `list(reversed([1,2,3]))` → [3,2,1] |
| `enumerate()` | 带索引遍历 | `for i,v in enumerate(list):` |
| `zip()` | 配对遍历 | `for a,b in zip(l1,l2):` |
| `map()` | 映射 | `map(func, list)` |
| `filter()` | 过滤 | `filter(func, list)` |
| `any()` | 任一为True | `any([False, True])` → True |
| `all()` | 全部为True | `all([True, False])` → False |
| `isinstance()` | 类型检查 | `isinstance(42, int)` → True |

---

## 本章小结

| 概念 | 说明 | 示例 |
|------|------|------|
| `def` | 定义函数 | `def add(a, b):` |
| `return` | 返回值 | `return a + b` |
| 位置参数 | 按顺序传 | `func(1, 2)` |
| 关键字参数 | 按名字传 | `func(a=1, b=2)` |
| 默认参数 | 可省略 | `def f(x=10):` |
| `*args` | 收集位置参数 | `def f(*args):` |
| `**kwargs` | 收集关键字参数 | `def f(**kw):` |
| 作用域 | 变量的可见范围 | local/global |
| `lambda` | 匿名函数 | `lambda x: x * 2` |
| 递归 | 函数调用自身 | `factorial(n-1)` |
| 高阶函数 | 函数作为参数 | `map/filter/sorted` |

---

## 下一步

进入 [第 7 章：模块与包](../07-modules-and-packages/README.md)。
