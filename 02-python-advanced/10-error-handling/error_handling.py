# 第 10 章配套代码：错误处理与调试
# 运行方式：python error_handling.py

import logging

# ============================
# 1. try/except
# ============================
print("=== try/except ===")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("  除数不能为零")

try:
    number = int("abc")
except ValueError as e:
    print(f"  转换失败: {e}")

# ============================
# 2. 完整 try/except/else/finally
# ============================
print("\n=== 完整 try 语句 ===")
test_values = [10, 3, 10, 0]
for a, b in zip(test_values[::2], test_values[1::2]):
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"  {a}/{b} -> 错误：除数不能为零")
    else:
        print(f"  {a}/{b} = {result:.4f}")
    finally:
        print("  计算结束")

# ============================
# 3. raise
# ============================
print("\n=== raise ===")


def set_age(age):
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")
    if age < 0 or age > 150:
        raise ValueError("年龄必须在 0-150 之间")
    return age


for test_age in [25, -5, "二十"]:
    try:
        set_age(test_age)
        print(f"  年龄 {test_age} 验证通过")
    except (ValueError, TypeError) as e:
        print(f"  年龄 {test_age} 验证失败: {e}")

# ============================
# 4. 自定义异常
# ============================
print("\n=== 自定义异常 ===")


class ValidationError(Exception):
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
    validate_email("invalid")
except ValidationError as e:
    print(f"  {e}")

# ============================
# 5. logging
# ============================
print("\n=== logging ===")
logging.basicConfig(level=logging.INFO, format="  %(levelname)s: %(message)s")
logging.info("程序正常运行")
logging.warning("这是一个警告")
logging.error("这是一个错误")
