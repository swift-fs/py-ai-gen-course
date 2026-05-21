# 第 1 章：变量与数据类型

> **学习目标**：理解变量的概念，掌握四种基本数据类型（整数、浮点数、字符串、布尔值），学会类型转换。

---

## 1. 什么是变量？

**变量**是存储数据的"盒子"。你给盒子贴个标签（变量名），往里面放东西（值），之后通过标签就能找到东西。

```python
name = "小明"
age = 18
height = 1.75
is_student = True
```

- `=` 是**赋值**（把右边的值放进左边的变量）
- ⚠️ 这不是数学的"等于"！`age = 18` 的意思是"把 18 存入 age"
- 变量一旦创建，就可以反复使用

```python
score = 95
print(score)         # 95
print(score + 5)     # 100（变量可以参与运算）
score = 88           # 变量的值可以改变
print(score)         # 88
```

---

## 2. 四种基本数据类型

### 整数（int）

没有小数点的数字：

```python
age = 18
temperature = -5
population = 7_800_000_000   # 可以用下划线分隔大数字
print(type(age))              # <class 'int'>
```

### 浮点数（float）

有小数点的数字：

```python
price = 9.99
pi = 3.14159
scientific = 1.5e10           # 科学计数法：1.5 × 10^10
print(type(price))            # <class 'float'>
```

> 整数和浮点数统称为**数字类型**。`type()` 函数可以查看变量的类型。

### 字符串（str）

用引号包裹的一段文字：

```python
name = "小明"
city = '北京'
message = """这是
多行字符串"""       # 三引号可以写多行

# 单引号和双引号完全等价，选一个你喜欢的
print(type(name))    # <class 'str'>
```

### 布尔值（bool）

只有两个值：`True`（真）和 `False`（假）。首字母必须大写。

```python
is_student = True
is_raining = False

# 布尔值常来自比较运算
print(5 > 3)      # True
print(5 == 5)     # True（两个等号才是"比较相等"）
print(5 != 3)     # True（!= 表示"不等于"）

print(type(is_student))   # <class 'bool'>
```

---

## 3. 类型转换

不同类型之间可以互相转换：

```python
# 字符串 → 数字
age_text = "18"
age = int(age_text)          # 字符串转为整数
print(age + 1)               # 19

price_text = "9.99"
price = float(price_text)    # 字符串转为浮点数
print(price)                 # 9.99

# 数字 → 字符串
number = 42
text = str(number)           # 数字转为字符串
print("答案是" + text)        # 答案是42（字符串用 + 拼接）

# 整数 ↔ 浮点数
print(int(3.9))     # 3（截断，不是四舍五入！）
print(float(5))     # 5.0
```

### 常见的转换错误

```python
# 不能把非数字字符串转为数字
# int("hello")    # ❌ ValueError!
# int("3.14")     # ❌ ValueError! 应该用 float("3.14")

# 布尔值可以转数字
print(int(True))    # 1
print(int(False))   # 0
```

---

## 4. f-string 格式化字符串

f-string 是把变量嵌入字符串的最简单方式——在引号前加 `f`，用 `{}` 放变量或表达式：

```python
name = "小明"
age = 18
height = 1.75

# 基本用法
print(f"我叫{name}，今年{age}岁")

# 可以放表达式
print(f"明年我就{age + 1}岁了")
print(f"身高{height:.1f}米")        # :.1f 表示保留1位小数
print(f"{'=' * 20}")                # 重复字符串
```

> `f"..."` 中的 `f` 代表 **format**（格式化）。这是 Python 3.6+ 引入的语法，推荐优先使用。

---

## 5. 变量命名规则

### 必须遵守的规则

```python
# ✅ 正确
name = "小明"
my_age = 18
score1 = 95
_student = True

# ❌ 错误（会报错）
# 1name = "小明"     数字不能开头
# my-name = "小明"   不能用减号
# my name = "小明"   不能有空格
# class = "A"        不能用 Python 关键字
```

### Python 关键字（不能用作变量名）

```python
# 这些是 Python 保留的关键字，不能用作变量名：
# if, else, for, while, def, class, import, return, True, False, None
# and, or, not, in, is, with, as, try, except, finally, raise
```

### 推荐的命名习惯

```python
# ✅ 好的命名：有意义，能看出是什么
student_name = "小明"
total_score = 95
is_passed = True

# ❌ 不好的命名：看不懂
a = "小明"
x = 95
flag = True
```

> Python 的命名习惯：全小写，单词之间用下划线连接。这叫 **snake_case**（蛇形命名）。

---

## 6. 同时赋值

Python 支持一些简洁的赋值方式：

```python
# 多变量同时赋值
x, y, z = 1, 2, 3
print(x, y, z)    # 1 2 3

# 交换两个变量的值（不需要临时变量）
x, y = y, x
print(x, y)       # 2 1

# 多个变量赋相同的值
a = b = c = 0
```

---

## 本章小结

| 类型 | 关键字 | 示例 | 说明 |
|------|--------|------|------|
| 整数 | `int` | `age = 18` | 没有小数点 |
| 浮点数 | `float` | `price = 9.99` | 有小数点 |
| 字符串 | `str` | `name = "小明"` | 引号包裹 |
| 布尔值 | `bool` | `is_ok = True` | True 或 False |

| 概念 | 说明 | 示例 |
|------|------|------|
| 变量 | 存储数据的"盒子" | `name = "小明"` |
| `type()` | 查看类型 | `type(42)` |
| `int()` `float()` `str()` | 类型转换 | `int("18")` |
| f-string | 格式化字符串 | `f"我叫{name}"` |
| snake_case | 推荐的命名方式 | `student_name` |

---

## 下一步

进入 [第 2 章：运算符与表达式](../02-operators/README.md)。
