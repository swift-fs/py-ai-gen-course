# 第 4 章配套代码：数据结构
# 运行方式：python data_structures.py

# ============================
# 1. 列表
# ============================
print("=== 列表 ===")
fruits = ["苹果", "香蕉", "橙子"]
print(f"原始: {fruits}")

fruits.append("葡萄")
print(f"append: {fruits}")

fruits.insert(1, "芒果")
print(f"insert(1,'芒果'): {fruits}")

fruits.remove("香蕉")
print(f"remove('香蕉'): {fruits}")

last = fruits.pop()
print(f"pop(): {last}, 剩余: {fruits}")

print(f"长度: {len(fruits)}")
print(f"'橙子' in fruits: {'橙子' in fruits}")

# 排序
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"sorted: {sorted(numbers)}")
print(f"sorted降序: {sorted(numbers, reverse=True)}")

# 列表推导式
squares = [x ** 2 for x in range(1, 6)]
print(f"平方: {squares}")
evens = [x for x in range(1, 11) if x % 2 == 0]
print(f"偶数: {evens}")

# 复制
original = [1, 2, 3]
copy1 = original.copy()
copy1[0] = 99
print(f"original: {original}, copy: {copy1}")

# ============================
# 2. 元组
# ============================
print("\n=== 元组 ===")
point = (3, 4)
print(f"元组: {point}")
print(f"point[0]: {point[0]}")

x, y = point
print(f"解包: x={x}, y={y}")

name, age = "小明", 18
print(f"多返回值: {name}, {age}")

# ============================
# 3. 字典
# ============================
print("\n=== 字典 ===")
student = {"name": "小明", "age": 18}
print(f"原始: {student}")
print(f"get('name'): {student.get('name')}")
print(f"get('email','无'): {student.get('email', '无')}")

student["email"] = "xm@example.com"
student.update({"age": 19, "city": "北京"})
print(f"更新后: {student}")

student.setdefault("grade", "A")
print(f"setdefault: {student}")

print("遍历:")
for key, value in student.items():
    print(f"  {key}: {value}")

squares_dict = {x: x ** 2 for x in range(1, 6)}
print(f"字典推导式: {squares_dict}")

# ============================
# 4. 集合
# ============================
print("\n=== 集合 ===")
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(f"交集 a & b: {a & b}")
print(f"并集 a | b: {a | b}")
print(f"差集 a - b: {a - b}")
print(f"对称差 a ^ b: {a ^ b}")

names = ["小明", "小红", "小明", "小刚"]
unique = set(names)
print(f"去重: {list(unique)}")

# ============================
# 5. 嵌套数据结构
# ============================
print("\n=== 嵌套结构 ===")
students = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]
for s in students:
    print(f"  {s['name']}: {s['score']}分")

by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print(f"按分数排序: {[s['name'] for s in by_score]}")
