# 第 12 章配套代码：生成器与迭代器
# 运行方式：python generators.py

import itertools

# ============================
# 1. 迭代器基础
# ============================
print("=== 迭代器 ===")
numbers = [1, 2, 3]
it = iter(numbers)
print(f"  next: {next(it)}")
print(f"  next: {next(it)}")
print(f"  next: {next(it)}")

# ============================
# 2. 生成器函数
# ============================
print("\n=== 生成器函数 ===")


def count_up(max_value):
    current = 1
    while current <= max_value:
        yield current
        current += 1


for num in count_up(5):
    print(f"  {num}", end=" ")
print()

# ============================
# 3. 生成器表达式
# ============================
print("\n=== 生成器表达式 ===")
squares = (x**2 for x in range(5))
print(f"  类型: {type(squares)}")
print(f"  列表: {list(squares)}")

total = sum(x**2 for x in range(10))
print(f"  平方和: {total}")

# ============================
# 4. 斐波那契生成器
# ============================
print("\n=== 斐波那契生成器 ===")


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()
first_ten = [next(fib) for _ in range(10)]
print(f"  前10个: {first_ten}")

# ============================
# 5. itertools
# ============================
print("\n=== itertools ===")
combined = list(itertools.chain([1, 2], [3, 4]))
print(f"  chain: {combined}")

combos = list(itertools.combinations("ABC", 2))
print(f"  combinations: {combos}")

perms = list(itertools.permutations("AB", 2))
print(f"  permutations: {perms}")

students = [
    {"name": "小明", "grade": "A"},
    {"name": "小红", "grade": "B"},
    {"name": "小刚", "grade": "A"},
]
students.sort(key=lambda s: s["grade"])
for grade, group in itertools.groupby(students, key=lambda s: s["grade"]):
    names = [s["name"] for s in group]
    print(f"  {grade}组: {names}")

first_five = list(itertools.islice(range(100), 5))
print(f"  islice: {first_five}")
