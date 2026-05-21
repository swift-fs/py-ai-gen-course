# 第 13 章配套代码：类型注解
# 运行方式：python type_annotations.py

from dataclasses import dataclass
from typing import Optional

# ============================
# 1. 基本类型注解
# ============================
print("=== 基本类型注解 ===")
name: str = "小明"
age: int = 18
height: float = 1.75
print(f"  {name}, {age}岁, {height}m")

# ============================
# 2. 函数注解
# ============================
print("\n=== 函数注解 ===")
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str, formal: bool = False) -> str:
    if formal:
        return f"尊敬的{name}，您好"
    return f"你好，{name}"

print(f"  add(3, 5) = {add(3, 5)}")
print(f"  {greet('小明')}")
print(f"  {greet('小明', formal=True)}")

# ============================
# 3. Optional
# ============================
print("\n=== Optional ===")
def find_user(user_id: int) -> Optional[str]:
    users = {1: "小明", 2: "小红"}
    return users.get(user_id)

for uid in [1, 3]:
    user = find_user(uid)
    if user:
        print(f"  用户{uid}: {user}")
    else:
        print(f"  用户{uid}: 未找到")

# ============================
# 4. dataclass + 类型注解
# ============================
print("\n=== dataclass + 类型注解 ===")
@dataclass
class Student:
    name: str
    age: int
    scores: list
    email: str | None = None

    def average(self) -> float:
        return sum(self.scores) / len(self.scores)

s = Student("小明", 18, [88.0, 92.0, 85.0], "xm@example.com")
print(f"  {s.name}: 平均分 {s.average():.1f}, 邮箱 {s.email}")

# ============================
# 5. 容器类型注解
# ============================
print("\n=== 容器类型 ===")
names: list[str] = ["小明", "小红"]
scores: dict[str, int] = {"小明": 88, "小红": 95}
unique: set[int] = {1, 2, 3}
print(f"  names: {names}")
print(f"  scores: {scores}")
print(f"  unique: {unique}")
