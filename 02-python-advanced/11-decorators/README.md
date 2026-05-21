# 第 11 章：装饰器

> **学习目标**：理解闭包和装饰器，学会编写装饰器来增强函数功能。

---

## 1. 函数是对象

在 Python 中，函数是一等公民——可以赋值给变量、作为参数传递、作为返回值：

```python
def greet(name):
    return f"你好，{name}"

# 函数赋值给变量
say_hello = greet
print(say_hello("小明"))    # 你好，小明

# 函数作为参数
def apply(func, value):
    return func(value)

print(apply(greet, "小红"))    # 你好，小红

# 函数作为返回值
def get_greeter():
    return greet

my_greet = get_greeter()
print(my_greet("小刚"))    # 你好，小刚
```

---

## 2. 闭包

闭包是一个函数，它"记住"了外部作用域的变量：

```python
def make_multiplier(factor):
    """创建一个乘法函数"""
    def multiply(number):
        return number * factor    # 记住了外部的 factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))     # 10
print(triple(5))     # 15
```

---

## 3. 基本装饰器

装饰器是**接收一个函数，返回一个增强版函数**的高阶函数：

```python
def timer(func):
    """计时装饰器：测量函数执行时间"""
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行耗时: {end - start:.4f}秒")
        return result
    return wrapper

@timer    # 等价于 slow_function = timer(slow_function)
def slow_function():
    import time
    time.sleep(0.1)
    return "完成"

slow_function()    # slow_function 执行耗时: 0.1xxx秒
```

### 装饰器的本质

```python
@timer
def my_func():
    pass

# 等价于：
def my_func():
    pass
my_func = timer(my_func)
```

---

## 4. 带参数的装饰器

```python
def retry(max_attempts=3):
    """重试装饰器：失败时自动重试"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第{attempt}次失败: {e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable():
    import random
    if random.random() < 0.7:
        raise ConnectionError("连接失败")
    return "成功"
```

---

## 5. functools.wraps —— 保留原函数信息

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)    # 保留原函数的名称、文档字符串等
    def wrapper(*args, **kwargs):
        """wrapper 的文档"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def my_function():
    """这是原函数的文档"""
    pass

print(my_function.__name__)     # my_function（没有 @wraps 会显示 wrapper）
print(my_function.__doc__)      # 这是原函数的文档
```

> **始终使用 `@wraps`**，这是好习惯。

---

## 6. 实用装饰器示例

### 缓存装饰器

```python
def cache(func):
    """简单的缓存装饰器"""
    cached = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
            print(f"  计算 {args} 并缓存")
        else:
            print(f"  使用缓存 {args}")
        return cached[args]
    return wrapper

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 权限检查装饰器

```python
def require_login(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("is_logged_in"):
            raise PermissionError("请先登录")
        return func(user, *args, **kwargs)
    return wrapper

@require_login
def view_profile(user):
    print(f"欢迎，{user['name']}")

user = {"name": "小明", "is_logged_in": True}
view_profile(user)    # 欢迎，小明
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| 函数是对象 | 可以赋值、传参、返回 |
| 闭包 | 函数记住外部变量 |
| 装饰器 | 接收函数，返回增强版函数 |
| `@decorator` | 语法糖 |
| 带参数装饰器 | 三层嵌套 |
| `@wraps` | 保留原函数信息 |

---

## 下一步

进入 [第 12 章：生成器与迭代器](../12-generators/README.md)。
