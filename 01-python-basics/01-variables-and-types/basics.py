# 第 1 章配套代码：变量与数据类型
# 运行方式：python basics.py

# ============================
# 1. 变量
# ============================
print("=== 变量 ===")
name = "小明"
age = 18
height = 1.75
is_student = True

print(f"姓名: {name}")
print(f"年龄: {age}")
print(f"身高: {height}")
print(f"学生: {is_student}")

# 变量可以改变
score = 95
print(f"初始分数: {score}")
score = 88
print(f"修改分数: {score}")

# ============================
# 2. 四种数据类型
# ============================
print("\n=== 数据类型 ===")
print(f"type(42) = {type(42)}")
print(f"type(3.14) = {type(3.14)}")
print(f"type('hello') = {type('hello')}")
print(f"type(True) = {type(True)}")

# ============================
# 3. 类型转换
# ============================
print("\n=== 类型转换 ===")
age_text = "18"
age_number = int(age_text)
print(f"字符串 '{age_text}' -> 数字 {age_number + 1}")

number = 42
text = str(number)
print(f"数字 {number} -> 字符串 '{text}'")

print(f"int(3.9) = {int(3.9)}")
print(f"float(5) = {float(5)}")
print(f"int(True) = {int(True)}, int(False) = {int(False)}")

# ============================
# 4. f-string
# ============================
print("\n=== f-string ===")
print(f"我叫{name}，今年{age}岁")
print(f"明年{age + 1}岁")
print(f"身高: {height:.1f}米")
print(f"{'=' * 20}")

# ============================
# 5. 同时赋值
# ============================
print("\n=== 同时赋值 ===")
x, y, z = 1, 2, 3
print(f"x={x}, y={y}, z={z}")

x, y = y, x
print(f"交换后: x={x}, y={y}")

a = b = c = 0
print(f"a={a}, b={b}, c={c}")
