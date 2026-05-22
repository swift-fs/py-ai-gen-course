# 第 9 章配套代码：面向对象编程
# 运行方式：python oop.py

import math
from dataclasses import dataclass, field

# ============================
# 1. 类和对象
# ============================
print("=== 类和对象 ===")


class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"  {self.name}：汪汪！")

    def info(self):
        print(f"  我叫{self.name}，是{self.breed}")


dog1 = Dog("旺财", "金毛")
dog2 = Dog("小花", "柯基")
dog1.bark()
dog2.info()

# ============================
# 2. 继承
# ============================
print("\n=== 继承 ===")


class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name}发出了声音"


class Cat(Animal):
    def speak(self):
        return f"{self.name}：喵喵！"


cat = Cat("咪咪")
print(f"  {cat.speak()}")


class CollegeStudent:
    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major

    def info(self):
        print(f"  {self.name}, {self.age}岁, {self.major}专业")


cs = CollegeStudent("小明", 20, "计算机")
cs.info()

# ============================
# 3. 魔术方法
# ============================
print("\n=== 魔术方法 ===")


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self):
        return int((self.x**2 + self.y**2) ** 0.5)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(f"  v1 + v2 = {v1 + v2}")
print(f"  len(v1) = {len(v1)}")
print(f"  v1 == v2: {v1 == v2}")

# ============================
# 4. dataclass
# ============================
print("\n=== dataclass ===")


@dataclass
class Student:
    name: str
    age: int
    score: float = 0.0

    def is_passed(self):
        return self.score >= 60


s1 = Student("小明", 18, 88.5)
s2 = Student("小红", 17, 92.0)
print(f"  {s1}")
print(f"  s1 通过: {s1.is_passed()}")
print(f"  s1 == s2: {s1 == s2}")

# ============================
# 5. property
# ============================
print("\n=== @property ===")


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius**2


c = Circle(5)
print(f"  半径5, 面积: {c.area:.2f}")

# ============================
# 6. staticmethod / classmethod
# ============================
print("\n=== staticmethod / classmethod ===")


class MathHelper:
    PI = 3.14159

    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def circle_area(cls, radius):
        return cls.PI * radius**2


print(f"  add(3, 5) = {MathHelper.add(3, 5)}")
print(f"  circle_area(3) = {MathHelper.circle_area(3):.2f}")
