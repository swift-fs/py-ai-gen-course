# 第 3 章：字符串详解

> **学习目标**：全面掌握字符串操作——索引、切片、格式化、常用方法，这是实际编程中使用频率最高的数据类型。

---

## 1. 创建字符串

```python
# 三种创建方式
single = '单引号'
double = "双引号"
multi = """这是
多行
字符串"""

# 单引号和双引号完全等价
# 如果字符串里包含引号，用另一种引号包裹
print("他说：'你好'")     # 他说：'你好'
print('她说："你好"')     # 她说："你好"

# 转义字符
print("第一行\n第二行")     # \n 换行
print("C:\\Users\\name")    # \\ 表示一个反斜杠
print("tab\there")          # \t 制表符

# 原始字符串（r-string）：不转义
print(r"C:\Users\name")     # C:\Users\name（反斜杠就是反斜杠）
```

---

## 2. 索引——访问单个字符

字符串中的每个字符都有一个**编号**（索引），从 **0** 开始：

```
字符串：  H   e   l   l   o
索引：    0   1   2   3   4
反向索引：-5  -4  -3  -2  -1
```

```python
text = "Hello"
print(text[0])     # H（第一个字符）
print(text[4])     # o（第五个字符）
print(text[-1])    # o（最后一个字符）
print(text[-2])    # l（倒数第二个）

# ⚠️ 索引不能超出范围
# print(text[10])  # IndexError!
```

---

## 3. 切片——截取一段子字符串

### 基本切片 `[开始:结束]`

```python
text = "Hello, Python!"

print(text[0:5])     # Hello（索引 0-4，不包含 5）
print(text[7:13])    # Python
print(text[:5])      # Hello（省略开始 = 从头开始）
print(text[7:])      # Python!（省略结束 = 到末尾）
print(text[:])       # Hello, Python!（完整复制）
```

> 切片规则：**包含开始，不包含结束**。`[0:5]` 取的是索引 0、1、2、3、4。

### 带步长的切片 `[开始:结束:步长]`

```python
text = "ABCDEFGHIJ"

print(text[0:6:2])    # ACE（每隔2个取一个）
print(text[::2])      # ACEGI（从头到尾每隔2个）
print(text[::-1])     # JIHGFEDCBA（反转字符串！）
print(text[5::-1])    # FEDCBA（从索引5倒着取）
```

---

## 4. 字符串是不可变的

字符串一旦创建，**不能修改**其中的字符：

```python
text = "Hello"
# text[0] = "J"    # ❌ TypeError! 字符串不可变

# 需要修改？创建新字符串
text = "J" + text[1:]    # Jello（拼接新字符串）
print(text)
```

---

## 5. 常用字符串方法

### 查找和计数

```python
text = "Hello, Python! Python is great."

print(text.find("Python"))       # 7（第一次出现的位置）
print(text.find("Java"))         # -1（找不到返回 -1）
print(text.rfind("Python"))      # 15（从右边找）
print(text.count("Python"))      # 2（出现次数）
print(text.index("Python"))      # 7（和 find 类似，但找不到会报错）
```

### 判断

```python
filename = "photo.jpg"
print(filename.startswith("photo"))    # True（是否以...开头）
print(filename.endswith(".jpg"))       # True（是否以...结尾）

name = "小明"
print(name.isalpha())     # True（是否全是字母/汉字）

number = "123"
print(number.isdigit())   # True（是否全是数字）

text = "Hello World"
print(text.isupper())     # False（是否全大写）
print(text.islower())     # False（是否全小写）
```

### 变换

```python
text = "  Hello, Python!  "

print(text.strip())                   # "Hello, Python!"（去除两端空白）
print(text.lstrip())                  # "Hello, Python!  "（去除左端空白）
print(text.rstrip())                  # "  Hello, Python!"（去除右端空白）
print(text.upper())                   # "  HELLO, PYTHON!  "（全转大写）
print(text.lower())                   # "  hello, python!  "（全转小写）
print(text.title())                   # "  Hello, Python!  "（每个单词首字母大写）
print(text.swapcase())                # "  hELLO, pYTHON!  "（大小写互换）
print(text.replace("Python", "World")) # "  Hello, World!  "（替换）
```

### 拆分和连接

```python
# split() —— 按分隔符拆成列表
sentence = "小明，18岁，北京"
parts = sentence.split("，")
print(parts)                # ['小明', '18岁', '北京']

# 不指定分隔符时，按空白字符拆分
words = "Hello   World  Python".split()
print(words)                # ['Hello', 'World', 'Python']

# splitlines() —— 按换行拆分
lines = "第一行\n第二行\n第三行".splitlines()
print(lines)                # ['第一行', '第二行', '第三行']

# join() —— 用指定字符连接列表
words = ["Hello", "World"]
print(" ".join(words))      # Hello World
print("-".join(words))      # Hello-World
print("".join(words))       # HelloWorld
```

### 对齐

```python
text = "Python"
print(text.center(20, "-"))    # -------Python-------
print(text.ljust(20, "."))     # Python..............
print(text.rjust(20, "."))     # ..............Python
print(f"{text:>20}")           #               Python（f-string 右对齐）
print(f"{text:<20}")           # Python              （f-string 左对齐）
print(f"{text:^20}")           #        Python       （f-string 居中）
```

---

## 6. 格式化字符串的几种方式

### f-string（推荐）

```python
name = "小明"
age = 18
pi = 3.14159

print(f"我叫{name}，今年{age}岁")
print(f"圆周率: {pi:.2f}")         # 3.14（保留2位小数）
print(f"{'姓名':<6}{'年龄':>4}")   # 姓名    年龄（对齐）
print(f"数字: {42:08d}")           # 00000042（补零）
```

### format() 方法

```python
# 旧式写法，仍然常见
print("我叫{}，今年{}岁".format("小明", 18))
print("我叫{0}，今年{1}岁，{0}很帅".format("小明", 18))
print("我叫{name}，今年{age}岁".format(name="小明", age=18))
```

---

## 7. 字符串常用操作速查表

| 方法             | 作用       | 示例                                 |
| ---------------- | ---------- | ------------------------------------ |
| `len(s)`         | 长度       | `len("hello")` → 5                   |
| `s[i]`           | 索引       | `"hello"[0]` → 'h'                   |
| `s[a:b]`         | 切片       | `"hello"[1:3]` → 'el'                |
| `s[::-1]`        | 反转       | `"hello"[::-1]` → 'olleh'            |
| `s.strip()`      | 去空白     | `" hi ".strip()` → 'hi'              |
| `s.upper()`      | 转大写     | `"Hi".upper()` → 'HI'                |
| `s.lower()`      | 转小写     | `"Hi".lower()` → 'hi'                |
| `s.replace(a,b)` | 替换       | `"hi".replace("h","H")` → 'Hi'       |
| `s.split(sep)`   | 拆分       | `"a,b,c".split(",")` → ['a','b','c'] |
| `sep.join(list)` | 连接       | `",".join(["a","b"])` → 'a,b'        |
| `s.find(sub)`    | 查找位置   | `"hello".find("ll")` → 2             |
| `s.count(sub)`   | 计数       | `"aba".count("a")` → 2               |
| `s.startswith()` | 开头判断   | `"hello".startswith("he")` → True    |
| `s.endswith()`   | 结尾判断   | `"hi.txt".endswith(".txt")` → True   |
| `s in text`      | 包含判断   | `"ell" in "hello"` → True            |
| `s.isdigit()`    | 是否全数字 | `"123".isdigit()` → True             |
| `s.isalpha()`    | 是否全字母 | `"abc".isalpha()` → True             |

---

## 本章小结

- 字符串是不可变的序列，用引号创建
- 索引从 0 开始，`[-1]` 是最后一个字符
- 切片 `[开始:结束:步长]`，`[::-1]` 反转
- 大量内置方法：`split/join/replace/strip/find/count/upper/lower`
- f-string 是最推荐的格式化方式

---

## 下一步

进入 [第 4 章：数据结构](../04-data-structures/README.md)。
