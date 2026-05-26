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

# --- 4.1 对比：普通类 vs dataclass ---
print("\n=== dataclass：普通类 vs dataclass ===")


# 传统写法：需要手写 __init__, __repr__, __eq__
class StudentOld:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def __repr__(self):
        return f"StudentOld(name={self.name!r}, age={self.age}, score={self.score})"

    def __eq__(self, other):
        if not isinstance(other, StudentOld):
            return False
        return self.name == other.name and self.age == other.age and self.score == other.score


# dataclass 写法：自动生成 __init__, __repr__, __eq__
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
print(f"  s1 == Student('小明', 18, 88.5): {s1 == Student('小明', 18, 88.5)}")

# --- 4.4 可变默认值：field(default_factory=...) ---
print("\n=== dataclass：field(default_factory=...) ===")


@dataclass
class ClassRoom:
    name: str
    students: list = field(default_factory=list)

    def add_student(self, student_name):
        self.students.append(student_name)


room1 = ClassRoom("三年二班")
room1.add_student("小明")
room1.add_student("小红")
room2 = ClassRoom("四年一班")
room2.add_student("小刚")
print(f"  {room1.name}: {room1.students}")
print(f"  {room2.name}: {room2.students}")

# --- 4.5 实战案例：商品购物车 ---
print("\n=== dataclass 实战：商品购物车 ===")


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 1

    @property
    def total(self):
        return self.price * self.quantity


@dataclass
class ShoppingCart:
    items: list = field(default_factory=list)

    def add_item(self, product: Product):
        self.items.append(product)

    @property
    def total_price(self):
        return sum(item.total for item in self.items)


cart = ShoppingCart()
cart.add_item(Product("Python编程书", 59.8, 2))
cart.add_item(Product("机械键盘", 299.0))
cart.add_item(Product("鼠标垫", 19.9, 3))
for item in cart.items:
    print(f"  {item.name} x{item.quantity} = ¥{item.total:.2f}")
print(f"  总计: ¥{cart.total_price:.2f}")

# --- 4.6 dataclass 继承 ---
print("\n=== dataclass 继承 ===")


@dataclass
class Person:
    name: str
    age: int


@dataclass
class Employee(Person):
    department: str
    salary: float = 0.0


emp = Employee("小明", 25, "技术部", 15000)
print(f"  {emp}")

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
