# 第 9 章：面向对象编程

> **学习目标**：理解类和对象的概念，掌握继承、魔术方法、dataclass、属性装饰器。

---

## 1. 什么是类和对象？

**类**是蓝图（设计图），**对象**是根据蓝图创建的具体实例。

```python
# 定义类
class Dog:
    def __init__(self, name, breed):
        self.name = name      # 属性（实例变量）
        self.breed = breed

    def bark(self):           # 方法
        print(f"{self.name}：汪汪！")

    def info(self):
        print(f"我叫{self.name}，是{self.breed}")

# 创建对象（实例化）
dog1 = Dog("旺财", "金毛")
dog2 = Dog("小花", "柯基")

dog1.bark()     # 旺财：汪汪！
dog2.info()     # 我叫小花，是柯基
```

### __init__ 和 self

- `__init__` 是**初始化方法**，创建对象时自动调用
- `self` 代表**对象自身**，类似于"我"
- 通过 `self.属性名` 访问对象的属性

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        if self.score >= 90:
            return "A"
        elif self.score >= 60:
            return "B"
        else:
            return "C"

s = Student("小明", 88)
print(s.get_grade())    # B
```

---

## 2. 继承

子类继承父类的属性和方法，还可以扩展或覆盖：

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name}发出了声音"

class Cat(Animal):
    def speak(self):           # 覆盖父类方法
        return f"{self.name}：喵喵！"

class Dog(Animal):
    def speak(self):
        return f"{self.name}：汪汪！"

    def fetch(self):           # 子类新增方法
        return f"{self.name}去捡球了"

cat = Cat("咪咪")
dog = Dog("旺财")
print(cat.speak())     # 咪咪：喵喵！
print(dog.speak())     # 旺财：汪汪！
print(dog.fetch())     # 旺财去捡球了
```

### super() —— 调用父类方法

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class CollegeStudent(Student):
    def __init__(self, name, age, major):
        super().__init__(name, age)    # 调用父类的 __init__
        self.major = major             # 子类新增属性

    def info(self):
        print(f"{self.name}, {self.age}岁, {self.major}专业")

cs = CollegeStudent("小明", 20, "计算机")
cs.info()
```

---

## 3. 魔术方法（Dunder Methods）

以 `__` 开头和结尾的特殊方法，让自定义类支持内置操作：

### __str__ 和 __repr__

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):          # print() 和 str() 调用
        return f"Point({self.x}, {self.y})"

    def __repr__(self):         # 调试时显示（更详细）
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(p)            # Point(3, 4)（调用 __str__）
print(repr(p))      # Point(x=3, y=4)（调用 __repr__）
```

### 运算符重载

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):       # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self):              # len(v)
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

    def __eq__(self, other):        # v1 == v2
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1 + v2)       # Vector(4, 6)
print(len(v1))       # 5
print(v1 == v2)      # False
```

### 常用魔术方法速查

| 方法 | 触发操作 | 示例 |
|------|---------|------|
| `__init__` | 创建对象 | `obj = MyClass()` |
| `__str__` | `print(obj)` | 用户友好的字符串 |
| `__repr__` | `repr(obj)` | 调试用的字符串 |
| `__len__` | `len(obj)` | 返回长度 |
| `__add__` | `obj1 + obj2` | 加法 |
| `__eq__` | `obj1 == obj2` | 相等比较 |
| `__lt__` | `obj1 < obj2` | 小于比较 |
| `__getitem__` | `obj[key]` | 索引访问 |
| `__setitem__` | `obj[key] = val` | 索引赋值 |
| `__contains__` | `val in obj` | 成员判断 |
| `__iter__` | `for x in obj` | 迭代 |
| `__call__` | `obj()` | 像函数一样调用 |

---

## 4. dataclass —— 自动生成样板代码

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    score: float = 0.0    # 默认值

    def is_passed(self):
        return self.score >= 60

# 自动生成 __init__, __repr__, __eq__
s1 = Student("小明", 18, 88.5)
s2 = Student("小红", 17, 92.0)

print(s1)                  # Student(name='小明', age=18, score=88.5)
print(s1.is_passed())      # True
print(s1 == s2)            # False（自动比较所有字段）
```

### dataclass 进阶

```python
from dataclasses import dataclass, field

@dataclass
class ClassRoom:
    name: str
    students: list = field(default_factory=list)  # 可变默认值

    def add_student(self, student):
        self.students.append(student)

room = ClassRoom("三年二班")
room.add_student("小明")
room.add_student("小红")
print(room.students)    # ['小明', '小红']
```

---

## 5. @property —— 把方法变成属性

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        """面积（像属性一样访问，不用加括号）"""
        import math
        return math.pi * self.radius ** 2

    @property
    def diameter(self):
        return 2 * self.radius

c = Circle(5)
print(c.area)       # 78.53...（不用写 c.area()）
print(c.diameter)   # 10
```

### 带 setter 的 property

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(t.fahrenheit)     # 77.0
t.celsius = 30          # 通过 setter 设置
# t.celsius = -300      # ValueError!
```

---

## 6. @staticmethod 和 @classmethod

```python
class MathHelper:
    PI = 3.14159    # 类变量（所有实例共享）

    @staticmethod
    def add(a, b):
        """静态方法：不需要 self，和类无关的实用函数"""
        return a + b

    @classmethod
    def from_value(cls, value):
        """类方法：第一个参数是类本身（cls）"""
        return cls.PI * value

print(MathHelper.add(3, 5))         # 8
print(MathHelper.from_value(2))     # 6.28...
```

### classmethod 的常见用途：替代构造函数

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, info_str):
        """从字符串创建对象"""
        name, age = info_str.split(",")
        return cls(name.strip(), int(age.strip()))

    def __repr__(self):
        return f"Student({self.name}, {self.age})"

s = Student.from_string("小明, 18")
print(s)    # Student(小明, 18)
```

---

## 7. 访问控制约定

Python 没有真正的"私有"，用命名约定表示：

```python
class MyClass:
    public_var = "公开"          # 公开（随意访问）
    _protected_var = "受保护"    # 约定：内部使用，不建议外部访问
    __private_var = "私有"       # 名称修饰：更难从外部访问

    def _internal_method(self):
        """内部方法，不建议外部调用"""
        pass
```

---

## 本章小结

| 概念 | 说明 | 示例 |
|------|------|------|
| `class` | 定义类 | `class Dog:` |
| `__init__` | 初始化方法 | `def __init__(self, name):` |
| `self` | 实例自身 | `self.name = name` |
| 继承 | 子类继承父类 | `class Cat(Animal):` |
| `super()` | 调用父类方法 | `super().__init__()` |
| `@dataclass` | 自动生成样板代码 | `@dataclass class Student:` |
| `__str__` | print 显示 | `def __str__(self):` |
| `__add__` | + 运算 | `def __add__(self, other):` |
| `@property` | 方法变属性 | `c.area` 不用括号 |
| `@staticmethod` | 静态方法 | 不需要 self |
| `@classmethod` | 类方法 | 第一个参数是 cls |

---

## 下一步

进入 [第 10 章：错误处理与调试](../10-error-handling/README.md)。
