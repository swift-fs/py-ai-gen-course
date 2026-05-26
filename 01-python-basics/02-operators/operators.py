# 第 2 章配套代码：运算符与表达式
# 运行方式：python operators.py

# ============================
# 1. 算术运算符
# ============================
print("=== 算术运算 ===")
print(f"10 + 3 = {10 + 3}")
print(f"10 - 3 = {10 - 3}")
print(f"10 * 3 = {10 * 3}")
print(f"10 / 3 = {10 / 3}")
print(f"10 // 3 = {10 // 3}")
print(f"10 % 3 = {10 % 3}")
print(f"2 ** 3 = {2**3}")

# 整除和取余的妙用
total_seconds = 125
minutes = total_seconds // 60
seconds = total_seconds % 60
print(f"125秒 = {minutes}分{seconds}秒")

# 浮点精度
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"round(0.1 + 0.2, 1) = {round(0.1 + 0.2, 1)}")

# ============================
# 2. 比较运算符
# ============================
print("\n=== 比较运算 ===")
print(f"5 > 3: {5 > 3}")
print(f"5 == 5: {5 == 5}")
print(f"5 != 3: {5 != 3}")
print(f"'apple' < 'banana': {'apple' < 'banana'}")

# ============================
# 3. 逻辑运算符
# ============================
print("\n=== 逻辑运算 ===")
age = 20
has_ticket = True
print(f"age >= 18 and has_ticket: {age >= 18 and has_ticket}")

is_vip = False
has_coupon = True
print(f"is_vip or has_coupon: {is_vip or has_coupon}")

is_closed = False
print(f"not is_closed: {not is_closed}")

# ============================
# 4. 成员运算符
# ============================
print("\n=== 成员运算 ===")
fruits = ["苹果", "香蕉", "橙子"]
print(f"'苹果' in fruits: {'苹果' in fruits}")
print(f"'葡萄' in fruits: {'葡萄' in fruits}")

text = "Hello, Python!"
print(f"'Python' in text: {'Python' in text}")

student = {"name": "小明", "age": 18}
print(f"'name' in student: {'name' in student}")
print(f"'小明' in student: {'小明' in student}")

# ============================
# 5. 复合赋值
# ============================
print("\n=== 复合赋值 ===")
x = 10
x += 5
print(f"x += 5 -> {x}")
x *= 2
print(f"x *= 2 -> {x}")

# ============================
# 6. 三元表达式
# ============================
print("\n=== 三元表达式 ===")
score = 85
status = "成年" if age >= 18 else "未成年"
print(f"状态: {status}")

name = ""
display = name if name else "匿名"
print(f"显示名: {display}")

grade = "优秀" if score >= 90 else "良好" if score >= 80 else "及格"
print(f"等级: {grade}")
