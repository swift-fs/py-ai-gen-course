# 第 10 章：错误处理与调试

> **学习目标**：学会用 try/except 处理错误，自定义异常，使用 logging 记录日志，掌握调试技巧。

---

## 1. 为什么需要错误处理？

程序运行时难免出错——文件不存在、网络断开、用户输入错误。如果不处理，程序直接崩溃。错误处理让程序在出错时**优雅地应对**。

---

## 2. try/except 基本用法

```python
# 捕获特定异常
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为零")

# 捕获多种异常
try:
    number = int("abc")
except ValueError:
    print("不是有效的数字")
except TypeError:
    print("类型错误")

# 获取异常信息
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"出错: {e}")    # 出错: division by zero
```

---

## 3. 完整的 try 语句

```python
try:
    f = open("data.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("文件不存在")
else:
    # try 没有出错时执行
    print(f"读取成功: {len(content)} 个字符")
finally:
    # 无论是否出错都会执行（清理资源）
    print("操作完成")
```

| 部分 | 何时执行 |
|------|---------|
| `try` | 始终尝试执行 |
| `except` | 出错时执行 |
| `else` | 没出错时执行 |
| `finally` | 始终执行（用于清理资源） |

---

## 4. 常见异常类型

| 异常 | 原因 | 示例 |
|------|------|------|
| `ValueError` | 值不正确 | `int("abc")` |
| `TypeError` | 类型不匹配 | `"a" + 1` |
| `KeyError` | 字典键不存在 | `d["不存在"]` |
| `IndexError` | 索引超出范围 | `[1,2][10]` |
| `FileNotFoundError` | 文件不存在 | `open("x.txt")` |
| `ZeroDivisionError` | 除以零 | `1 / 0` |
| `AttributeError` | 属性不存在 | `"hi".xxx` |
| `ImportError` | 导入失败 | `import 不存在` |

---

## 5. raise —— 主动抛出异常

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")
    if age < 0 or age > 150:
        raise ValueError("年龄必须在 0-150 之间")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(f"错误: {e}")
```

---

## 6. 自定义异常

```python
class ValidationError(Exception):
    """自定义验证异常"""
    def __init__(self, message, field):
        self.message = message
        self.field = field
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.field}] {self.message}"

def validate_email(email):
    if "@" not in email:
        raise ValidationError("邮箱格式不正确", "email")
    return email

try:
    validate_email("invalid-email")
except ValidationError as e:
    print(e)    # [email] 邮箱格式不正确
```

---

## 7. logging —— 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,          # 最低日志级别
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

logging.debug("调试信息")     # 开发调试用
logging.info("正常运行")      # 正常流程记录
logging.warning("警告")       # 需要注意但不影响运行
logging.error("错误")         # 出错了但程序还能继续
logging.critical("严重错误")  # 程序可能无法继续
```

> 生产环境通常设为 `logging.INFO` 或 `logging.WARNING`。

---

## 8. 调试技巧

### print 大法

```python
def calculate(data):
    print(f"DEBUG: data = {data}")      # 查看中间值
    result = sum(data) / len(data)
    print(f"DEBUG: result = {result}")
    return result
```

### 断言 assert

```python
def factorial(n):
    assert n >= 0, "n 不能为负数"    # 条件不满足时抛出 AssertionError
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

> `assert` 用于开发阶段检查假设。生产代码应该用 `if + raise`。

---

## 本章小结

| 概念 | 说明 |
|------|------|
| `try/except` | 捕获并处理异常 |
| `else` | 没出错时执行 |
| `finally` | 始终执行（清理资源） |
| `raise` | 主动抛出异常 |
| `assert` | 断言条件为真 |
| `logging` | 记录日志 |
| 自定义异常 | 继承 `Exception` |

---

## 下一步

进入 [第 11 章：装饰器](../11-decorators/README.md)。
