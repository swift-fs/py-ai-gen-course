# 第 11 章配套代码：装饰器
# 运行方式：python decorators.py

import time
from functools import wraps

# ============================
# 1. 函数是对象
# ============================
print("=== 函数是对象 ===")
def greet(name):
    return f"你好，{name}"

say_hello = greet
print(f"  {say_hello('小明')}")

def apply(func, value):
    return func(value)
print(f"  {apply(greet, '小红')}")

# ============================
# 2. 闭包
# ============================
print("\n=== 闭包 ===")
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(f"  double(5) = {double(5)}")
print(f"  triple(5) = {triple(5)}")

# ============================
# 3. 计时装饰器
# ============================
print("\n=== 计时装饰器 ===")
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  {func.__name__} 耗时: {elapsed:.4f}秒")
        return result
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(0.05)
    return a + b

result = slow_add(3, 5)
print(f"  结果: {result}")
print(f"  函数名: {slow_add.__name__}")

# ============================
# 4. 缓存装饰器
# ============================
print("\n=== 缓存装饰器 ===")
def cache(func):
    cached = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
            print(f"  计算 fibonacci{args}")
        return cached[args]
    return wrapper

@cache
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(f"  fib(10) = {fib(10)}")

# ============================
# 5. 重试装饰器
# ============================
print("\n=== 重试装饰器 ===")
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  第{attempt}次失败: {e}")
                    if attempt == max_attempts:
                        print(f"  达到最大重试次数")
                        return None
        return wrapper
    return decorator

import random
random.seed(42)

@retry(max_attempts=3)
def unstable():
    if random.random() < 0.5:
        raise ConnectionError("连接失败")
    return "成功"

print(f"  结果: {unstable()}")
