# random 标准库 —— 随机数与随机选择

> **学习目标**：掌握 `random` 模块的核心功能，能灵活生成随机数、做随机选择、打乱顺序，并理解伪随机数的概念和可重复性。

---

## 1. 什么是 random 模块？

`random` 是 Python 标准库中的一个模块，提供了**伪随机数生成器**（PRNG, Pseudo-Random Number Generator）。

所谓"伪随机"，是指这些数字并不是真正随机的，而是通过一个数学公式计算出来的。给定相同的"种子"（seed），每次运行都会得到完全相同的序列。对于大多数日常用途（游戏、抽奖、模拟）来说，这已经足够"随机"了。

> **安全提示**：如果你需要生成密码、令牌等安全敏感的随机值，请使用 `secrets` 模块而不是 `random`。

---

## 2. 导入方式

```python
import random
```

> 本教程中所有示例都假设你已经 `import random`。

---

## 3. 生成随机整数

### `random.randint(a, b)` —— 最常用的随机整数

返回一个随机整数 N，满足 `a <= N <= b`（**两端都包含**）。

```python
# 掷骰子（1 到 6）
dice = random.randint(1, 6)
print(f"骰子点数: {dice}")

# 随机选一个 -10 到 10 之间的整数
number = random.randint(-10, 10)
print(f"随机整数: {number}")
```

### `random.randrange(start, stop[, step])` —— 更灵活的整数范围

和 `range()` 函数的参数一样，返回从 `range(start, stop, step)` 中随机选一个元素。**不包含 stop**。

```python
# 0 到 9 之间的随机整数（不包含 10）
n = random.randrange(10)
print(n)

# 1 到 99 之间的随机奇数
odd = random.randrange(1, 100, 2)
print(f"随机奇数: {odd}")

# 0 到 100 之间 5 的倍数
multiple_of_5 = random.randrange(0, 101, 5)
print(f"5 的倍数: {multiple_of_5}")
```

### 对比 `randint` vs `randrange`

| 特性     | `randint(a, b)`     | `randrange(start, stop, step)` |
| -------- | ------------------- | ------------------------------ |
| 终止值   | **包含** b          | **不包含** stop                |
| 步长     | 不支持              | 支持                           |
| 等价写法 | `randrange(a, b+1)` | —                              |

---

## 4. 生成随机浮点数

### `random.random()` —— 0 到 1 之间的随机浮点数

返回 `[0.0, 1.0)` 之间的随机浮点数（包含 0.0，**不包含** 1.0）。

```python
x = random.random()
print(f"随机浮点数: {x}")  # 例如: 0.7134258901234567
```

### `random.uniform(a, b)` —— 指定范围的随机浮点数

返回 `[a, b]`（或 `[b, a]`，取决于谁大）之间的随机浮点数。

```python
# 随机温度（20.0 到 35.0 度）
temperature = random.uniform(20.0, 35.0)
print(f"随机温度: {temperature:.1f}°C")

# 也可以 a > b
price = random.uniform(100, 50)
print(f"随机价格: {price:.2f} 元")
```

---

## 5. 从序列中随机选择

### `random.choice(seq)` —— 随机选一个元素

从一个非空序列（列表、元组、字符串等）中随机选一个元素。

```python
# 随机选一种水果
fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
fruit = random.choice(fruits)
print(f"今天吃: {fruit}")

# 从字符串中随机选一个字符
char = random.choice("ABCDEFG")
print(f"随机字母: {char}")
```

> **注意**：如果序列为空，会抛出 `IndexError`。

### `random.choices(population, weights=None, k=1)` —— 随机选多个（可重复）

从序列中随机选 `k` 个元素，**允许重复**（选完放回去再选）。可以通过 `weights` 设置权重。

```python
colors = ["红色", "蓝色", "绿色"]

# 随机选 3 个（可能重复）
selected = random.choices(colors, k=3)
print(f"选中的颜色: {selected}")  # 例如: ['蓝色', '红色', '蓝色']

# 带权重的选择——红色概率更高
lottery = random.choices(colors, weights=[5, 3, 2], k=10)
print(f"10 次抽奖: {lottery}")
```

**权重说明**：`weights=[5, 3, 2]` 表示红色占总权重 5/(5+3+2) = 50%，蓝色 30%，绿色 20%。

### `random.sample(population, k)` —— 随机选多个（不重复）

从序列中随机选 `k` 个**不重复**的元素（选完不放回）。相当于不放回抽样。

```python
# 从 1-49 中选 6 个不重复的号码（彩票）
numbers = random.sample(range(1, 50), 6)
print(f"彩票号码: {sorted(numbers)}")

# 从班级中随机抽 3 人
students = ["小明", "小红", "小华", "小丽", "小刚", "小芳"]
group = random.sample(students, 3)
print(f"小组成员: {group}")
```

> **注意**：`k` 不能大于序列长度，否则抛出 `ValueError`。

### `choices` vs `sample` 对比

| 特性       | `choices(seq, k=n)` | `sample(seq, k=n)` |
| ---------- | ------------------- | ------------------ |
| 是否可重复 | **可以**重复        | **不可**重复       |
| 支持权重   | 支持 `weights`      | 不支持             |
| k 的限制   | 可以大于序列长度    | 不能大于序列长度   |
| 使用场景   | 模拟多次独立实验    | 抽奖、抽样调查     |

---

## 6. 打乱序列顺序

### `random.shuffle(x)` —— 原地打乱

将序列**原地**打乱顺序（直接修改原序列，不返回新序列）。

```python
# 洗牌
cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
random.shuffle(cards)
print(f"洗牌后: {cards}")

# 随机排座次
students = ["小明", "小红", "小华", "小丽", "小刚"]
random.shuffle(students)
print(f"座位顺序: {students}")
```

> **注意**：`shuffle` 只能用于**可变序列**（如列表），不能用于字符串或元组。

如果你不想修改原序列，可以先复制一份：

```python
original = [1, 2, 3, 4, 5]
shuffled = original.copy()
random.shuffle(shuffled)
print(f"原序列: {original}")   # [1, 2, 3, 4, 5]
print(f"打乱后: {shuffled}")   # 例如: [3, 1, 5, 2, 4]
```

---

## 7. 随机种子 —— 让结果可重复

### `random.seed(a=None)` —— 设置随机种子

设置种子后，后续的随机操作会得到**完全相同**的结果。这在调试和测试时非常有用。

```python
# 设置种子
random.seed(42)
print(random.randint(1, 100))  # 总是输出相同的数字
print(random.choice(["A", "B", "C"]))  # 总是相同的选项

# 重置为相同的种子，序列会从头开始
random.seed(42)
print(random.randint(1, 100))  # 和上面第一个一样
```

**什么时候用 seed？**

- **调试**：让 bug 可以稳定复现
- **测试**：让单元测试结果可预测
- **演示**：让教程示例每次运行都一样
- **科学实验**：让模拟实验可重复

**什么时候不用？**

- 正常的程序运行中不需要手动设置种子
- Python 会自动使用系统时间等作为种子

---

## 8. 其他分布的随机数

`random` 还提供了多种概率分布的随机数生成函数。如果你不懂这些数学概念，可以先跳过，需要时再回来查阅。

### 正态分布（高斯分布）`random.gauss(mu, sigma)` / `random.normalvariate(mu, sigma)`

生成符合正态分布的随机数。`mu` 是均值，`sigma` 是标准差。

```python
# 模拟考试成绩（均值 75，标准差 10）
scores = [random.gauss(75, 10) for _ in range(10)]
print("模拟成绩:", [f"{s:.1f}" for s in scores])
```

### 三角分布 `random.triangular(low, high, mode)`

生成三角分布的随机数。`mode` 是最可能出现的值（峰值）。

```python
# 模拟通勤时间（最少 20 分钟，最多 60 分钟，通常 35 分钟）
commute = random.triangular(20, 60, 35)
print(f"通勤时间: {commute:.1f} 分钟")
```

### 指数分布 `random.expovariate(lambd)`

生成指数分布的随机数。常用于模拟等待时间。`lambd` 是速率参数（注意不是 λ 的倒数）。

```python
# 模拟客服来电间隔（平均每 5 分钟一个电话，lambd = 1/5 = 0.2）
interval = random.expovariate(0.2)
print(f"距下一个电话: {interval:.1f} 分钟")
```

---

## 9. 实用示例

### 示例 1：猜数字游戏

```python
import random

secret = random.randint(1, 100)
print("我想了一个 1-100 的数字，你来猜！")

while True:
    guess = int(input("你的猜测: "))

    if guess < secret:
        print("太小了！")
    elif guess > secret:
        print("太大了！")
    else:
        print("恭喜你，猜对了！")
        break
```

### 示例 2：随机密码生成器

```python
import random
import string

def generate_password(length=16):
    # 可用字符：字母 + 数字 + 特殊符号
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    # 随机选择不重复的字符
    password = "".join(random.choices(characters, k=length))
    return password

print(f"随机密码: {generate_password()}")
print(f"8 位密码: {generate_password(8)}")
```

### 示例 3：随机分组

```python
import random

def random_groups(people, group_count):
    random.shuffle(people)
    groups = [[] for _ in range(group_count)]
    for index, person in enumerate(people):
        groups[index % group_count].append(person)
    return groups

students = ["小明", "小红", "小华", "小丽", "小刚", "小芳", "小李", "小王"]
groups = random_groups(students, 3)

for group_number, group in enumerate(groups, 1):
    print(f"第 {group_number} 组: {', '.join(group)}")
```

### 示例 4：简易抽签器

```python
import random

items = [
    {"name": "一等奖", "count": 1},
    {"name": "二等奖", "count": 3},
    {"name": "三等奖", "count": 5},
    {"name": "谢谢参与", "count": 20},
]

# 构建奖池
pool = []
for item in items:
    pool.extend([item["name"]] * item["count"])

result = random.choice(pool)
print(f"抽奖结果: {result}")
```

---

## 10. 常用函数速查表

| 函数                            | 说明                    | 示例                           |
| ------------------------------- | ----------------------- | ------------------------------ |
| `random()`                      | [0.0, 1.0) 的随机浮点数 | `random.random()`              |
| `randint(a, b)`                 | [a, b] 的随机整数       | `random.randint(1, 10)`        |
| `randrange(start, stop, step)`  | 指定范围的随机整数      | `random.randrange(0, 100, 5)`  |
| `uniform(a, b)`                 | [a, b] 的随机浮点数     | `random.uniform(1.0, 10.0)`    |
| `choice(seq)`                   | 随机选一个元素          | `random.choice([1,2,3])`       |
| `choices(seq, k=n, weights=[])` | 随机选多个（可重复）    | `random.choices([1,2,3], k=5)` |
| `sample(seq, k=n)`              | 随机选多个（不重复）    | `random.sample([1,2,3], k=2)`  |
| `shuffle(list)`                 | 原地打乱列表顺序        | `random.shuffle([1,2,3])`      |
| `seed(n)`                       | 设置随机种子            | `random.seed(42)`              |
| `gauss(mu, sigma)`              | 正态分布随机数          | `random.gauss(0, 1)`           |

---

## 11. 常见问题

### Q：每次运行结果都不一样，正常吗？

**正常**。默认情况下，Python 使用系统时间作为种子，所以每次运行结果都不同。如果需要每次结果相同，在开头加 `random.seed(42)`（或任何固定数字）。

### Q：`randint(1, 10)` 包含 10 吗？

**包含**。`randint(a, b)` 两端都包含，所以 `randint(1, 10)` 可能返回 1 到 10 之间的任何整数，包括 1 和 10。

### Q：怎么从字典中随机选一个键？

```python
scores = {"小明": 95, "小红": 88, "小华": 92}
name = random.choice(list(scores.keys()))
print(f"随机选到: {name}, 分数: {scores[name]}")
```

### Q：`random` 能用于加密吗？

**不能**。`random` 是伪随机数，理论上可以被预测。密码、令牌等安全场景请使用 `secrets` 模块：

```python
import secrets

# 生成安全的随机令牌
token = secrets.token_hex(16)
print(f"安全令牌: {token}")
```

---

## 返回

[← 返回模块与包](./README.md)
