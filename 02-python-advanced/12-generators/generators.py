# 第 12 章配套代码：生成器与迭代器
# 运行方式：python generators.py

import itertools

# ============================
# 1. 迭代器基础
# ============================
print("=== 1. 迭代器基础 ===")

numbers = [1, 2, 3]
it = iter(numbers)  # 获取迭代器
print(f"  next: {next(it)}")  # 1
print(f"  next: {next(it)}")  # 2
print(f"  next: {next(it)}")  # 3

# 迭代器只能用一次
numbers2 = [1, 2, 3]
it2 = iter(numbers2)
print(f"  第一次 list(it): {list(it2)}")  # [1, 2, 3]
print(f"  第二次 list(it): {list(it2)}")  # [] —— 已用完
print(f"  原始列表不变: {numbers2}")  # [1, 2, 3]

# ============================
# 2. 生成器函数
# ============================
print("\n=== 2. 生成器函数 ===")


# 用 yield 暂停函数，逐个产生值
def count_up(max_value):
    """生成从 1 到 max_value 的数字"""
    current = 1
    while current <= max_value:
        yield current  # 暂停在这里，交出 current
        current += 1  # 下次从这里继续


# 调用生成器函数，返回的是生成器对象，不会立即执行
gen = count_up(3)
print(f"  类型: {type(gen)}")  # <class 'generator'>

# 用 next() 逐个取值
print(f"  next: {next(gen)}")  # 1
print(f"  next: {next(gen)}")  # 2
print(f"  next: {next(gen)}")  # 3

# 更常见：直接用 for 循环遍历
print("  for循环:", end=" ")
for num in count_up(5):
    print(num, end=" ")  # 1 2 3 4 5
print()

# ============================
# 3. 生成器表达式
# ============================
print("\n=== 3. 生成器表达式 ===")

# 列表推导式 vs 生成器表达式（圆括号代替方括号）
squares_list = [x**2 for x in range(5)]
squares_gen = (x**2 for x in range(5))

print(f"  列表推导式类型: {type(squares_list)}")  # <class 'list'>
print(f"  生成器表达式类型: {type(squares_gen)}")  # <class 'generator'>
print(f"  列表推导式结果: {squares_list}")  # [0, 1, 4, 9, 16]
print(f"  生成器转列表: {list(squares_gen)}")  # [0, 1, 4, 9, 16]

# 常用场景：配合 sum() 等聚合函数，省内存
total = sum(x**2 for x in range(10))
print(f"  平方和(0-9): {total}")  # 285

# ============================
# 4. 实用生成器示例
# ============================
print("\n=== 4. 实用生成器示例 ===")


# 4.1 斐波那契数列 —— 无限序列
def fibonacci():
    """无限斐波那契数列生成器"""
    a, b = 0, 1
    while True:  # 无限循环，但 yield 会暂停，不会卡住
        yield a
        a, b = b, a + b


fib = fibonacci()
first_ten = [next(fib) for _ in range(10)]
print(f"  斐波那契前10个: {first_ten}")  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# 4.2 数据管道 —— 生成器组合
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
        yield n**2


# 管道：数字 → 过滤偶数 → 求平方
pipeline = square(filter_even(get_numbers()))
print(f"  管道结果: {list(pipeline)}")  # [4, 16, 36, 64, 100]

# ============================
# 5. itertools 常用工具
# ============================
print("\n=== 5. itertools ===")

# chain —— 连接多个可迭代对象
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print(f"  chain: {combined}")  # [1, 2, 3, 4, 5]

# combinations —— 组合（不考虑顺序）
combos = list(itertools.combinations("ABC", 2))
print(f"  combinations: {combos}")  # [('A','B'), ('A','C'), ('B','C')]

# permutations —— 排列（考虑顺序）
perms = list(itertools.permutations("AB", 2))
print(f"  permutations: {perms}")  # [('A','B'), ('B','A')]

# groupby —— 分组（注意：必须先排序！）
students = [
    {"name": "小明", "grade": "A"},
    {"name": "小红", "grade": "B"},
    {"name": "小刚", "grade": "A"},
]
students.sort(key=lambda s: s["grade"])  # 排序是必须的
for grade, group in itertools.groupby(students, key=lambda s: s["grade"]):
    names = [s["name"] for s in group]
    print(f"  {grade}组: {names}")

# islice —— 对迭代器切片
first_five = list(itertools.islice(range(100), 5))
print(f"  islice: {first_five}")  # [0, 1, 2, 3, 4]

# ============================
# 6. 常见错误演示
# ============================
print("\n=== 6. 常见错误 ===")

# 错误1：生成器是一次性的
gen_once = (x for x in range(3))
print(f"  第一次: {list(gen_once)}")  # [0, 1, 2]
print(f"  第二次: {list(gen_once)}")  # [] —— 空了

# 错误2：groupby 前忘记排序
data = [("A", 1), ("B", 2), ("A", 3)]
print("  未排序的 groupby 结果:")
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"    {key}: {list(group)}")  # A 会被分成两组

# 错误3：生成器不能用 len()
gen_no_len = (x for x in range(5))
try:
    _ = len(gen_no_len)
except TypeError as e:
    print(f"  len(生成器) 报错: {e}")
print(f"  正确做法: len(list(gen)) = {len(list((x for x in range(5))))}")
