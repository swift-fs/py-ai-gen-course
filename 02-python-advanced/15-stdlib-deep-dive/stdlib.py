# 第 15 章配套代码：标准库深入
# 运行方式：python stdlib.py

import re
from collections import Counter, defaultdict, namedtuple
from functools import reduce, partial, lru_cache
from pathlib import Path

# ============================
# 1. re 正则表达式
# ============================
print("=== re 正则 ===")
text = "电话138-1234-5678，邮箱test@example.com"
phones = re.findall(r"\d{3}-\d{4}-\d{4}", text)
print(f"  电话: {phones}")
emails = re.findall(r"[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-zA-Z]+", text)
print(f"  邮箱: {emails}")

hidden = re.sub(r"\d{4}", "****", "138-1234-5678")
print(f"  隐藏: {hidden}")

m = re.search(r"(\d+)分", "成绩95分")
if m:
    print(f"  分数: {m.group(1)}")

# ============================
# 2. collections
# ============================
print("\n=== Counter ===")
words = ["苹果", "香蕉", "苹果", "橙子", "香蕉", "苹果"]
count = Counter(words)
print(f"  计数: {count}")
print(f"  最多的2个: {count.most_common(2)}")

print("\n=== defaultdict ===")
grades = defaultdict(list)
grades["小明"].extend([95, 88])
grades["小红"].append(92)
print(f"  成绩: {dict(grades)}")

print("\n=== namedtuple ===")
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"  Point: x={p.x}, y={p.y}")
print(f"  索引: [{p[0]}, {p[1]}]")

# ============================
# 3. functools
# ============================
print("\n=== functools ===")
numbers = [1, 2, 3, 4, 5]
print(f"  reduce求和: {reduce(lambda a, b: a + b, numbers)}")


def power(base, exponent):
    return base**exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(f"  square(5) = {square(5)}")
print(f"  cube(3) = {cube(3)}")


@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(f"  fib(30) = {fibonacci(30)}")
print(f"  缓存: {fibonacci.cache_info()}")

# ============================
# 4. pathlib 进阶
# ============================
print("\n=== pathlib ===")
p = Path("/home/user/docs/report.txt")
print(f"  父目录: {p.parent}")
print(f"  文件名: {p.name}")
print(f"  stem: {p.stem}")
print(f"  后缀: {p.suffix}")
