# 第 7 章配套代码：模块与包
# 运行方式：python modules.py

# ============================
# 1. import 方式
# ============================
print("=== import 方式 ===")
import random

print(f"random.randint(1,10): {random.randint(1, 10)}")

from math import pi, sqrt

print(f"pi = {pi}")
print(f"sqrt(16) = {sqrt(16)}")

import datetime as dt

print(f"现在: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================
# 2. 常用标准库
# ============================
print("\n=== random ===")
fruits = ["苹果", "香蕉", "橙子"]
print(f"随机选: {random.choice(fruits)}")

items = [1, 2, 3, 4, 5]
random.shuffle(items)
print(f"打乱: {items}")

print("\n=== math ===")
import math

print(f"ceil(3.2) = {math.ceil(3.2)}")
print(f"floor(3.8) = {math.floor(3.8)}")

print("\n=== datetime ===")
from datetime import datetime, timedelta

now = datetime.now()
print(f"今天: {now.strftime('%Y-%m-%d')}")
print(f"明天: {(now + timedelta(days=1)).strftime('%Y-%m-%d')}")

print("\n=== pathlib ===")
from pathlib import Path

cwd = Path.cwd()
print(f"当前目录: {cwd}")
print(f"父目录: {cwd.parent}")

print("\n=== json ===")
import json

data = {"name": "小明", "scores": [95, 88]}
text = json.dumps(data, ensure_ascii=False)
print(f"序列化: {text}")
parsed = json.loads(text)
print(f"反序列化: {parsed['name']}, 分数: {parsed['scores']}")

# ============================
# 3. __name__ 演示
# ============================
print("\n=== __name__ ===")
print(f"当前 __name__ = {__name__}")
import calculator.basic

# from calculator.basic import add, subtract
from calculator import add, subtract

if __name__ == "__main__":
    print("  这个文件是被直接运行的")
    print(f"add(1,2) = {calculator.basic.add(1, 2)}")
    print(f"add(1,2) = {add(1, 2)}")
    print(f"subtract(1,2) = {calculator.basic.subtract(1, 2)}")
    print(f"subtract(1,2) = {subtract(1, 2)}")
    print(f"power(2,3) = {calculator.advanced.power(2, 3)}")
