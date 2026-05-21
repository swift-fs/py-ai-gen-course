# 第 2 章：运算符与表达式

> **学习目标**：掌握所有常用运算符（算术、比较、逻辑、成员、赋值），理解运算优先级，学会三元表达式。

---

## 1. 算术运算符

```python
print(10 + 3)     # 13    加法
print(10 - 3)     # 7     减法
print(10 * 3)     # 30    乘法
print(10 / 3)     # 3.333...  除法（结果总是浮点数）
print(10 // 3)    # 3     整除（只保留整数部分）
print(10 % 3)     # 1     取余数（模运算）
print(2 ** 3)     # 8     幂运算（2的3次方）
print(9 ** 0.5)   # 3.0   开方（9的0.5次方）
```

### 整除和取余的妙用

```python
# 把秒数转为分和秒
total_seconds = 125
minutes = total_seconds // 60    # 整除：2 分钟
seconds = total_seconds % 60     # 取余：5 秒
print(f"{minutes}分{seconds}秒")

# 判断奇偶
number = 7
if number % 2 == 0:
    print("偶数")
else:
    print("奇数")
```

### 数字精度问题

```python
# 浮点数运算可能有精度误差
print(0.1 + 0.2)         # 0.30000000000000004（不是精确的 0.3！）
print(round(0.1 + 0.2, 1))  # 0.3（用 round() 四舍五入）
```

> 这是所有编程语言的共同问题，不是 Python 的 bug。原因是浮点数在计算机中以二进制存储。

---

## 2. 比较运算符

比较运算符的结果是**布尔值**（True 或 False）：

```python
print(5 > 3)       # True   大于
print(5 < 3)       # False  小于
print(5 >= 5)      # True   大于或等于
print(5 <= 3)      # False  小于或等于
print(5 == 5)      # True   等于（两个等号！）
print(5 != 3)      # True   不等于
```

> ⚠️ **最常见错误**：判断相等用 `==`（两个等号），一个等号 `=` 是赋值！

### 比较字符串

```python
print("apple" == "apple")     # True
print("apple" != "banana")    # True
print("apple" < "banana")     # True（按字母顺序比较）
print("A" < "a")              # True（大写字母的编码值更小）
```

---

## 3. 逻辑运算符

用于组合多个条件：

### and —— 并且（两个条件都满足）

```python
age = 20
has_ticket = True

# 两个条件都为 True，结果才是 True
print(age >= 18 and has_ticket)     # True（满足入场条件）
print(age >= 18 and not has_ticket) # False（没票不行）
```

### or —— 或者（满足一个就行）

```python
is_vip = False
has_coupon = True

# 只要有一个为 True，结果就是 True
print(is_vip or has_coupon)    # True（有优惠券就行）
```

### not —— 取反

```python
is_closed = False
print(not is_closed)    # True（没关门 = 开着）
```

### 短路求值

```python
# and：遇到 False 就停，后面的不执行
result = False and print("这行不会执行")

# or：遇到 True 就停，后面的不执行
result = True or print("这行不会执行")
```

---

## 4. 成员运算符

判断某个值是否在序列中（列表、字符串、元组、集合、字典）：

```python
# in —— 是否包含
fruits = ["苹果", "香蕉", "橙子"]
print("苹果" in fruits)       # True
print("葡萄" in fruits)       # False

# 字符串中也可以用
text = "Hello, Python!"
print("Python" in text)       # True

# not in —— 是否不包含
print("葡萄" not in fruits)   # True

# 字典中 in 检查的是键
student = {"name": "小明", "age": 18}
print("name" in student)      # True（检查键）
print("小明" in student)      # False（不检查值！）
```

---

## 5. 赋值运算符

### 基本赋值和复合赋值

```python
x = 10

x += 5     # 等价于 x = x + 5，x 变成 15
x -= 3     # 等价于 x = x - 3，x 变成 12
x *= 2     # 等价于 x = x * 2，x 变成 24
x //= 5    # 等价于 x = x // 5，x 变成 4
x **= 3    # 等价于 x = x ** 3，x 变成 64
x %= 10    # 等价于 x = x % 10，x 变成 4
```

> `+=` 是最常用的复合赋值，特别是在循环中计数时。

### 海象运算符 `:=`（Python 3.8+）

在表达式中同时赋值：

```python
# 传统写法
text = "Hello"
length = len(text)
if length > 3:
    print(f"字符串长度 {length} 大于 3")

# 海象运算符写法（一行搞定）
if (length := len(text)) > 3:
    print(f"字符串长度 {length} 大于 3")
```

---

## 6. 运算优先级

当一行代码有多个运算符时，Python 按优先级执行（从高到低）：

| 优先级 | 运算符 | 说明 |
|--------|--------|------|
| 1（最高） | `**` | 幂运算 |
| 2 | `+x`, `-x` | 正号、负号 |
| 3 | `*`, `/`, `//`, `%` | 乘除、整除、取余 |
| 4 | `+`, `-` | 加减 |
| 5 | `<`, `<=`, `>`, `>=`, `==`, `!=` | 比较运算 |
| 6 | `not` | 逻辑非 |
| 7 | `and` | 逻辑与 |
| 8（最低） | `or` | 逻辑或 |

**建议**：不确定优先级时，**加括号**！括号让意图更清晰。

```python
# 不确定？加括号！
result = (2 + 3) * 4      # 20（括号优先）
result = 2 + 3 * 4         # 14（乘法优先）

# 复杂条件也建议加括号
if (age >= 18) and (has_ticket or is_vip):
    print("可以入场")
```

---

## 7. 三元表达式

三元表达式是 if-else 的**单行简写**：

```python
# 普通 if-else
age = 20
if age >= 18:
    status = "成年"
else:
    status = "未成年"

# 三元表达式（一行搞定）
status = "成年" if age >= 18 else "未成年"
print(status)    # 成年

# 常见用法：设置默认值
name = ""
display = name if name else "匿名"
print(display)    # 匿名

# 嵌套（不推荐，可读性差）
score = 85
grade = "优秀" if score >= 90 else "良好" if score >= 80 else "及格"
print(grade)    # 良好
```

**语法**：`值A if 条件 else 值B`
- 条件为 True → 返回值 A
- 条件为 False → 返回值 B

---

## 本章小结

| 类别 | 运算符 | 示例 |
|------|--------|------|
| 算术 | `+ - * / // % **` | `10 // 3` → 3 |
| 比较 | `> < >= <= == !=` | `5 > 3` → True |
| 逻辑 | `and or not` | `True and False` → False |
| 成员 | `in not in` | `"a" in "abc"` → True |
| 赋值 | `= += -= *= /=` | `x += 1` |
| 三元 | `A if 条件 else B` | `"大" if x > 0 else "小"` |

---

## 下一步

进入 [第 3 章：字符串详解](../03-strings/README.md)。
