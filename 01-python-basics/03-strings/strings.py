# 第 3 章配套代码：字符串详解
# 运行方式：python strings.py

# ============================
# 1. 创建和基本操作
# ============================
print("=== 创建字符串 ===")
text = "Hello, Python!"
print(text)
print(f"长度: {len(text)}")
print(f"类型: {type(text)}")

# ============================
# 2. 索引
# ============================
print("\n=== 索引 ===")
print(f"text[0] = {text[0]}")
print(f"text[-1] = {text[-1]}")
print(f"text[7] = {text[7]}")

# ============================
# 3. 切片
# ============================
print("\n=== 切片 ===")
print(f"text[0:5] = {text[0:5]}")
print(f"text[7:] = {text[7:]}")
print(f"text[:5] = {text[:5]}")
print(f"text[::-1] = {text[::-1]}")
print(f"text[::2] = {text[::2]}")

# ============================
# 4. 常用方法
# ============================
print("\n=== 常用方法 ===")
sample = "  Hello, Python! Python is great.  "
print(f"strip: '{sample.strip()}'")
print(f"upper: '{sample.upper()}'")
print(f"lower: '{sample.lower()}'")
print(f"replace: '{sample.replace('Python', 'World')}'")
print(f"find('Python'): {sample.find('Python')}")
print(f"count('Python'): {sample.count('Python')}")

# ============================
# 5. 拆分和连接
# ============================
print("\n=== 拆分和连接 ===")
sentence = "小明，18岁，北京"
parts = sentence.split("，")
print(f"split: {parts}")

words = ["Hello", "World"]
print(f"join空格: {' '.join(words)}")
print(f"join横线: {'-'.join(words)}")

# ============================
# 6. 判断方法
# ============================
print("\n=== 判断方法 ===")
print(f"'photo.jpg'.endswith('.jpg'): {'photo.jpg'.endswith('.jpg')}")
print(f"'123'.isdigit(): {'123'.isdigit()}")
print(f"'abc'.isalpha(): {'abc'.isalpha()}")
print(f"'Python' in text: {'Python' in text}")

# ============================
# 7. 格式化
# ============================
print("\n=== 格式化 ===")
name = "小明"
age = 18
pi = 3.14159

print(f"我叫{name}，今年{age}岁")
print(f"圆周率: {pi:.2f}")
print(f"补零: {42:08d}")
print(f"{'姓名':<6}|{'年龄':>4}")
