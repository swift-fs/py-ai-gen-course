# 第 5 章：控制流

> **学习目标**：掌握条件判断和循环——让程序能"做决定"和"重复执行"。

---

## 1. if 条件判断

### 基本 if-elif-else

```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

**执行逻辑**：从上往下依次检查条件，**第一个满足的条件执行后，后面的全部跳过**。

### 注意事项

```python
# ⚠️ 缩进很重要！Python 用缩进表示代码块
if True:
    print("这行属于 if")     # 4个空格缩进
    print("这行也属于 if")   # 同一级别的缩进
print("这行不属于 if")       # 没有缩进，在 if 外面

# 可以只有 if
if score > 100:
    print("数据异常")

# if-else
age = 20
if age >= 18:
    print("成年")
else:
    print("未成年")
```

### 条件组合

```python
age = 25
income = 8000

# and：两个条件都要满足
if age >= 18 and income >= 5000:
    print("符合条件")

# or：满足一个就行
if age < 18 or age > 65:
    print("特殊人群")

# not：取反
is_closed = False
if not is_closed:
    print("正在营业")
```

---

## 2. for 循环

### 基本用法

```python
# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"我喜欢{fruit}")

# 遍历字符串
for char in "Hello":
    print(char)

# 遍历字典
student = {"name": "小明", "age": 18}
for key, value in student.items():
    print(f"{key}: {value}")
```

### range() —— 生成数字序列

```python
# range(结束) —— 0 到 结束-1
for i in range(5):
    print(i)    # 0, 1, 2, 3, 4

# range(开始, 结束) —— 开始 到 结束-1
for i in range(2, 6):
    print(i)    # 2, 3, 4, 5

# range(开始, 结束, 步长)
for i in range(0, 10, 2):
    print(i)    # 0, 2, 4, 6, 8

# 倒序
for i in range(5, 0, -1):
    print(i)    # 5, 4, 3, 2, 1
```

### enumerate() —— 同时获取索引和值

```python
fruits = ["苹果", "香蕉", "橙子"]
for index, fruit in enumerate(fruits):
    print(f"第{index + 1}个: {fruit}")
```

### zip() —— 同时遍历多个列表

```python
names = ["小明", "小红", "小刚"]
scores = [88, 95, 72]

for name, score in zip(names, scores):
    print(f"{name}: {score}分")
```

---

## 3. while 循环

```python
# 基本用法：条件为 True 时一直执行
count = 0
while count < 5:
    print(f"第{count + 1}次")
    count += 1    # ⚠️ 别忘了改变条件，否则死循环！
```

### while 适合的场景

```python
# 用户输入直到正确
password = ""
while password != "123456":
    password = input("请输入密码：")
print("登录成功！")

# 猜数字
import random
target = random.randint(1, 100)
guess = 0
while guess != target:
    guess = int(input("猜一个数字(1-100)："))
    if guess > target:
        print("大了")
    elif guess < target:
        print("小了")
print("猜对了！")
```

---

## 4. break 和 continue

### break —— 立即退出整个循环

```python
# 找到第一个偶数就停
numbers = [1, 3, 7, 4, 9, 2]
for n in numbers:
    if n % 2 == 0:
        print(f"找到偶数: {n}")
        break
# 输出：找到偶数: 4
```

### continue —— 跳过本次，继续下一次

```python
# 只打印奇数
for i in range(10):
    if i % 2 == 0:
        continue    # 偶数跳过
    print(i)         # 1 3 5 7 9
```

---

## 5. for-else 和 while-else

`else` 和循环搭配时，表示**循环正常结束**（没被 break）时执行：

```python
# 检查列表中是否有负数
numbers = [1, 3, 5, 7]

for n in numbers:
    if n < 0:
        print(f"发现负数: {n}")
        break
else:
    print("没有负数，全部为正")    # 循环没被 break，执行 else
```

> `else` 和 `for/while` 搭配有点反直觉。简单记：**没 break → 执行 else**。

---

## 6. pass 语句

`pass` 是一个**什么都不做的占位符**。当你需要写代码但还没想好写什么时：

```python
# 占位：以后再实现
def todo_function():
    pass

class MyError(Exception):
    pass

# 空的 if 分支
if debug_mode:
    pass    # 以后加调试代码
else:
    print("正常运行")
```

---

## 7. 常见陷阱

### 陷阱 1：修改正在遍历的列表

```python
# ❌ 错误：边遍历边删除会跳过元素
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
# 结果可能不是你想要的！

# ✅ 正确：创建副本再遍历
numbers = [1, 2, 3, 4, 5]
for n in numbers[:]:       # numbers[:] 是列表的副本
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)    # [1, 3, 5]

# ✅ 更好：用列表推导式
numbers = [1, 2, 3, 4, 5]
numbers = [n for n in numbers if n % 2 != 0]
```

### 陷阱 2：死循环

```python
# ❌ 忘了改变条件
# while True:
#     print("永远停不下来")

# ✅ 确保循环条件最终会变
count = 0
while count < 10:
    count += 1
```

### 陷阱 3：range 不是列表

```python
r = range(5)
print(r)           # range(0, 5)（不是 [0, 1, 2, 3, 4]！）
print(list(r))     # [0, 1, 2, 3, 4]（需要转成列表才能看到）
```

---

## 本章小结

| 语法 | 作用 | 示例 |
|------|------|------|
| `if/elif/else` | 条件判断 | `if score >= 60:` |
| `for` | 遍历序列 | `for item in list:` |
| `while` | 条件循环 | `while count < 10:` |
| `range()` | 生成数字序列 | `range(0, 10, 2)` |
| `enumerate()` | 同时获取索引和值 | `for i, v in enumerate(list):` |
| `zip()` | 同时遍历多个列表 | `for a, b in zip(list1, list2):` |
| `break` | 退出循环 | `break` |
| `continue` | 跳过本次 | `continue` |
| `for-else` | 循环没被 break 时执行 | `for ... else:` |
| `pass` | 占位符 | `pass` |

---

## 下一步

进入 [第 6 章：函数](../06-functions/README.md)。
