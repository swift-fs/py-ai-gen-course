# 第 6 章配套代码：函数
# 运行方式：python functions.py

# ============================
# 1. 基本函数
# ============================
print("=== 基本函数 ===")

def greet(name):
    print(f"你好，{name}！")

greet("小明")

def add(a, b):
    return a + b

print(f"add(3, 5) = {add(3, 5)}")

def divide(a, b):
    return a // b, a % b

q, r = divide(17, 5)
print(f"divide(17, 5) -> 商:{q}, 余:{r}")

# ============================
# 2. 参数类型
# ============================
print("\n=== 参数类型 ===")

def describe_pet(name, animal):
    print(f"  我有一只{animal}，叫{name}")

describe_pet("旺财", "狗")
describe_pet(animal="猫", name="小花")

def greet_with_default(name, greeting="你好"):
    print(f"  {greeting}，{name}！")

greet_with_default("小明")
greet_with_default("小明", "早上好")

# ============================
# 3. *args 和 **kwargs
# ============================
print("\n=== *args 和 **kwargs ===")

def add_all(*args):
    print(f"  收到: {args}, 求和: {sum(args)}")

add_all(1, 2, 3)
add_all(1, 2, 3, 4, 5)

def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="小明", age=18, city="北京")

# ============================
# 4. 作用域
# ============================
print("\n=== 作用域 ===")
message = "全局变量"

def scope_demo():
    message = "局部变量"
    print(f"  函数内: {message}")

scope_demo()
print(f"  函数外: {message}")

# ============================
# 5. lambda
# ============================
print("\n=== lambda ===")
square = lambda x: x ** 2
print(f"  square(5) = {square(5)}")

students = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]
by_score = sorted(students, key=lambda s: s["score"])
print(f"  按分数排序: {[s['name'] for s in by_score]}")

numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"  map翻倍: {doubled}")

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"  filter偶数: {evens}")

# ============================
# 6. 递归
# ============================
print("\n=== 递归 ===")

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"  5! = {factorial(5)}")

def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

fib_list = [fibonacci(i) for i in range(10)]
print(f"  斐波那契: {fib_list}")

# ============================
# 7. 常用内置函数
# ============================
print("\n=== 常用内置函数 ===")
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"  len: {len(nums)}")
print(f"  sum: {sum(nums)}")
print(f"  max: {max(nums)}")
print(f"  min: {min(nums)}")
print(f"  sorted: {sorted(nums)}")
print(f"  any: {any([False, True, False])}")
print(f"  all: {all([True, True, False])}")
