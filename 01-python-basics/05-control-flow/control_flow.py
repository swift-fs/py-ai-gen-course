# 第 5 章配套代码：控制流
# 运行方式：python control_flow.py

# ============================
# 1. if 条件判断
# ============================
print("=== if 条件判断 ===")
score = 85
if score >= 90:
    grade = "优秀"
elif score >= 80:
    grade = "良好"
elif score >= 60:
    grade = "及格"
else:
    grade = "不及格"
print(f"分数{score} -> {grade}")

# ============================
# 2. for 循环
# ============================
print("\n=== for 循环 ===")
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"  我喜欢{fruit}")

# range
print("range(5):", list(range(5)))
print("range(2,6):", list(range(2, 6)))
print("range(0,10,2):", list(range(0, 10, 2)))

# enumerate
for index, fruit in enumerate(fruits):
    print(f"  第{index + 1}个: {fruit}")

# zip
names = ["小明", "小红", "小刚"]
scores = [88, 95, 72]
for name, s in zip(names, scores):
    print(f"  {name}: {s}分")

# ============================
# 3. while 循环
# ============================
print("\n=== while 循环 ===")
count = 0
while count < 5:
    count += 1
print(f"count = {count}")

# ============================
# 4. break 和 continue
# ============================
print("\n=== break ===")
numbers = [1, 3, 7, 4, 9, 2]
for n in numbers:
    if n % 2 == 0:
        print(f"  找到第一个偶数: {n}")
        break

print("\n=== continue ===")
for i in range(10):
    if i % 2 == 0:
        continue
    print(f"  {i}", end=" ")
print()

# ============================
# 5. for-else
# ============================
print("\n=== for-else ===")
numbers = [1, 3, 5, 7]
for n in numbers:
    if n < 0:
        print(f"  发现负数: {n}")
        break
else:
    print("  没有负数")

# ============================
# 6. 列表推导式（结合控制流）
# ============================
print("\n=== 列表推导式 ===")
squares = [x ** 2 for x in range(1, 6)]
print(f"  平方: {squares}")
evens = [x for x in range(1, 11) if x % 2 == 0]
print(f"  偶数: {evens}")
