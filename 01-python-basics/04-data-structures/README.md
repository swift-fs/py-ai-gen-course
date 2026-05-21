# 第 4 章：数据结构

> **学习目标**：掌握四种核心数据结构——列表、元组、字典、集合，以及嵌套数据结构。

---

## 1. 列表（list）—— 有序的可变序列

列表是 Python 中最常用的数据结构，用 `[]` 创建。

### 创建和访问

```python
# 创建列表
fruits = ["苹果", "香蕉", "橙子"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]   # 可以混合类型
empty = []                          # 空列表

# 访问元素（索引从 0 开始）
print(fruits[0])      # 苹果
print(fruits[-1])     # 橙子（最后一个）

# 切片（和字符串一样）
print(numbers[1:3])   # [2, 3]
print(numbers[::-1])  # [5, 4, 3, 2, 1]
```

### 修改元素

```python
fruits = ["苹果", "香蕉", "橙子"]

# 修改单个元素
fruits[0] = "草莓"
print(fruits)    # ['草莓', '香蕉', '橙子']

# 修改一段元素
fruits[1:3] = ["葡萄", "芒果"]
print(fruits)    # ['草莓', '葡萄', '芒果']
```

### 添加元素

```python
fruits = ["苹果", "香蕉"]

# append() —— 在末尾添加一个元素
fruits.append("橙子")
print(fruits)    # ['苹果', '香蕉', '橙子']

# insert() —— 在指定位置插入
fruits.insert(1, "葡萄")
print(fruits)    # ['苹果', '葡萄', '香蕉', '橙子']

# extend() —— 合并另一个列表
more = ["芒果", "西瓜"]
fruits.extend(more)
print(fruits)    # ['苹果', '葡萄', '香蕉', '橙子', '芒果', '西瓜']

# + 运算符也可以合并（创建新列表）
all_fruits = fruits + ["梨"]
```

### 删除元素

```python
fruits = ["苹果", "香蕉", "橙子", "香蕉"]

# remove() —— 删除第一个匹配的值
fruits.remove("香蕉")
print(fruits)    # ['苹果', '橙子', '香蕉']

# pop() —— 删除指定位置并返回该值
item = fruits.pop(0)
print(item)      # 苹果
print(fruits)    # ['橙子', '香蕉']

# pop() 不传参数则删除最后一个
last = fruits.pop()

# del —— 按索引删除
del fruits[0]

# clear() —— 清空整个列表
fruits.clear()
```

### 查找和计数

```python
fruits = ["苹果", "香蕉", "橙子", "香蕉"]

print(fruits.index("橙子"))     # 2（第一次出现的索引）
print(fruits.count("香蕉"))     # 2（出现次数）
print("苹果" in fruits)          # True
print(len(fruits))               # 4（列表长度）
```

### 排序

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# sorted() —— 返回新列表，不修改原列表
print(sorted(numbers))           # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(numbers, reverse=True))  # [9, 6, 5, 4, 3, 2, 1, 1]
print(numbers)                   # [3, 1, 4, 1, 5, 9, 2, 6]（原列表不变）

# sort() —— 直接修改原列表
numbers.sort()
print(numbers)                   # [1, 1, 2, 3, 4, 5, 6, 9]

# 按条件排序
students = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]
by_score = sorted(students, key=lambda s: s["score"])
print([s["name"] for s in by_score])   # ['小刚', '小明', '小红']
```

### 列表推导式

用一行代码从已有列表创建新列表：

```python
# 基本语法：[表达式 for 变量 in 可迭代对象]
squares = [x ** 2 for x in range(1, 6)]
print(squares)    # [1, 4, 9, 16, 25]

# 带条件过滤
even = [x for x in range(1, 11) if x % 2 == 0]
print(even)       # [2, 4, 6, 8, 10]

# 字符串列表转大写
names = ["alice", "bob", "charlie"]
upper_names = [name.upper() for name in names]
print(upper_names)    # ['ALICE', 'BOB', 'CHARLIE']
```

### 列表的复制

```python
original = [1, 2, 3]

# ❌ 直接赋值不是复制！两个变量指向同一个列表
wrong_copy = original
wrong_copy[0] = 99
print(original)    # [99, 2, 3]（原列表也被改了！）

# ✅ 正确的复制方式
copy1 = original.copy()          # 方法一：copy()
copy2 = original[:]              # 方法二：切片
copy3 = list(original)           # 方法三：list()
```

---

## 2. 元组（tuple）—— 有序的不可变序列

元组一旦创建，**不能修改**。用 `()` 创建。

```python
# 创建元组
point = (3, 4)
rgb = (255, 128, 0)
single = (42,)       # 注意：单个元素的元组必须加逗号！

# 访问（和列表一样用索引）
print(point[0])      # 3
print(point[-1])     # 4

# 不能修改
# point[0] = 5       # ❌ TypeError!

# 元组的用处
x, y = point         # 解包（unpacking）
print(f"x={x}, y={y}")

# 函数返回多个值
def get_user():
    return "小明", 18

name, age = get_user()
```

### 元组 vs 列表

| 特性 | 列表 `[]` | 元组 `()` |
|------|----------|----------|
| 可变性 | 可修改 | 不可修改 |
| 性能 | 稍慢 | 稍快 |
| 用途 | 数据会变化时 | 数据固定不变时 |
| 作为字典的键 | ❌ 不行 | ✅ 可以 |

---

## 3. 字典（dict）—— 键值对

字典用 `{}` 创建，每个元素是 `键: 值` 的配对。

### 创建和访问

```python
# 创建字典
student = {
    "name": "小明",
    "age": 18,
    "scores": [95, 88, 92]
}

# 通过键访问值
print(student["name"])          # 小明
print(student["scores"])        # [95, 88, 92]

# get() —— 安全访问（键不存在时不报错）
print(student.get("name"))           # 小明
print(student.get("email"))          # None（不存在返回 None）
print(student.get("email", "无"))    # 无（不存在返回默认值）
```

### 修改

```python
student = {"name": "小明", "age": 18}

# 添加或修改
student["email"] = "xm@example.com"   # 添加新键值对
student["age"] = 19                    # 修改已有键
print(student)

# update() —— 批量更新
student.update({"age": 20, "city": "北京"})
print(student)

# setdefault() —— 键不存在时设置默认值
student.setdefault("grade", "A")     # grade 不存在，设为 A
student.setdefault("grade", "B")     # grade 已存在，不修改
print(student["grade"])              # A
```

### 删除

```python
student = {"name": "小明", "age": 18, "email": "xm@example.com"}

del student["email"]              # 删除指定键
age = student.pop("age")          # 删除并返回值
print(age)                        # 18
```

### 遍历

```python
student = {"name": "小明", "age": 18, "city": "北京"}

# 遍历键
for key in student:
    print(key, student[key])

# 遍历键值对（推荐）
for key, value in student.items():
    print(f"{key}: {value}")

# 只遍历键
for key in student.keys():
    print(key)

# 只遍历值
for value in student.values():
    print(value)
```

### 字典推导式

```python
# 基本语法：{键表达式: 值表达式 for 变量 in 可迭代对象}
squares = {x: x ** 2 for x in range(1, 6)}
print(squares)    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 从两个列表创建字典
keys = ["name", "age", "city"]
values = ["小明", 18, "北京"]
student = dict(zip(keys, values))
print(student)    # {'name': '小明', 'age': 18, 'city': '北京'}
```

---

## 4. 集合（set）—— 无序的不重复元素

集合的特点：**元素不重复**、**无序**（不能用索引访问）。

### 创建

```python
# 创建集合
colors = {"红", "绿", "蓝"}
numbers = {1, 2, 3, 2, 1}    # 自动去重
print(numbers)                 # {1, 2, 3}

# 从列表去重
names = ["小明", "小红", "小明", "小刚"]
unique = set(names)
print(unique)                  # {'小明', '小红', '小刚'}
print(list(unique))            # 转回列表

# 空集合只能用 set() 创建
empty = set()    # ✅
# empty = {}     # ❌ 这是空字典！
```

### 常用操作

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# 交集（两个集合都有的）
print(a & b)          # {3, 4}
print(a.intersection(b))   # {3, 4}

# 并集（两个集合的所有元素）
print(a | b)          # {1, 2, 3, 4, 5, 6}
print(a.union(b))     # {1, 2, 3, 4, 5, 6}

# 差集（a 有但 b 没有的）
print(a - b)          # {1, 2}
print(a.difference(b))  # {1, 2}

# 对称差集（只在其中一个集合中出现的）
print(a ^ b)          # {1, 2, 5, 6}

# 添加和删除
a.add(5)
a.discard(1)    # 删除元素（不存在也不报错）
# a.remove(99)  # 删除元素（不存在会报错）
```

### 集合推导式

```python
squares = {x ** 2 for x in range(-3, 4)}
print(squares)    # {0, 1, 4, 9}（自动去重）
```

---

## 5. 嵌套数据结构

实际编程中，数据经常嵌套使用：

### 列表里放字典

```python
students = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]

# 访问
print(students[1]["name"])     # 小红

# 遍历
for student in students:
    print(f"{student['name']}: {student['score']}分")
```

### 字典里放列表

```python
# 班级成绩表
grades = {
    "数学": [88, 92, 76, 95],
    "语文": [85, 90, 78, 88],
}

# 每科的平均分
for subject, scores in grades.items():
    avg = sum(scores) / len(scores)
    print(f"{subject}平均分: {avg:.1f}")
```

### 字典嵌套字典

```python
users = {
    "xiaoming": {"name": "小明", "age": 18, "city": "北京"},
    "xiaohong": {"name": "小红", "age": 17, "city": "上海"},
}

print(users["xiaoming"]["city"])    # 北京
```

---

## 6. 四种数据结构对比

| 特性 | 列表 `[]` | 元组 `()` | 字典 `{k:v}` | 集合 `{}` |
|------|----------|----------|-------------|----------|
| 有序 | ✅ | ✅ | ✅ (3.7+) | ❌ |
| 可变 | ✅ | ❌ | ✅ | ✅ |
| 可重复 | ✅ | ✅ | 键不可重复 | ❌ |
| 索引访问 | ✅ | ✅ | 按键访问 | ❌ |
| 用途 | 有序数据集合 | 不可变数据 | 键值映射 | 去重、集合运算 |

---

## 本章小结

- **列表**：最常用，有序可变，支持增删改查、排序、推导式
- **元组**：不可变，适合固定数据、函数返回多值
- **字典**：键值对，查找快，适合映射关系
- **集合**：自动去重，支持交并差运算
- **嵌套结构**：列表+字典的组合在实际中非常常见

---

## 下一步

进入 [第 5 章：控制流](../05-control-flow/README.md)。
