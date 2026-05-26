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

| 方法           | 触发操作         | 示例              |
| -------------- | ---------------- | ----------------- |
| `__init__`     | 创建对象         | `obj = MyClass()` |
| `__str__`      | `print(obj)`     | 用户友好的字符串  |
| `__repr__`     | `repr(obj)`      | 调试用的字符串    |
| `__len__`      | `len(obj)`       | 返回长度          |
| `__add__`      | `obj1 + obj2`    | 加法              |
| `__eq__`       | `obj1 == obj2`   | 相等比较          |
| `__lt__`       | `obj1 < obj2`    | 小于比较          |
| `__getitem__`  | `obj[key]`       | 索引访问          |
| `__setitem__`  | `obj[key] = val` | 索引赋值          |
| `__contains__` | `val in obj`     | 成员判断          |
| `__iter__`     | `for x in obj`   | 迭代              |
| `__call__`     | `obj()`          | 像函数一样调用    |

---

## 4. dataclass —— 自动生成样板代码

### 4.1 为什么要用 dataclass？

先看一个问题：用普通 class 定义一个"学生"，你需要写多少代码？

```python
# 😫 传统写法：手写一堆"样板代码"
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def __repr__(self):              # 为了 print 能好看
        return f"Student(name={self.name!r}, age={self.age}, score={self.score})"

    def __eq__(self, other):         # 为了能用 == 比较
        if not isinstance(other, Student):
            return False
        return self.name == other.name and self.age == other.age and self.score == other.score

s1 = Student("小明", 18, 88.5)
print(s1)              # Student(name='小明', age=18, score=88.5)
print(s1 == Student("小明", 18, 88.5))   # True
```

上面这些 `__init__`、`__repr__`、`__eq__` 都是"样板代码"——每个类都要写，但内容几乎一样，枯燥又容易出错。

**dataclass 就是帮你自动写这些样板代码的！** 同样的效果，只需要：

```python
# 😄 dataclass 写法：简洁多了！
from dataclasses import dataclass

@dataclass                    # 这个 @ 装饰器告诉 Python："帮我自动生成样板代码"
class Student:
    name: str                 # 字段名: 类型（类型注解，告诉 Python 这个字段存什么）
    age: int
    score: float

s1 = Student("小明", 18, 88.5)
print(s1)                     # Student(name='小明', age=18, score=88.5)  ← 自动生成了 __repr__
print(s1 == Student("小明", 18, 88.5))   # True  ← 自动生成了 __eq__
```

> **一句话理解**：`@dataclass` 就像一个"代码生成器"，你只写字段定义，它帮你自动生成 `__init__`、`__repr__`、`__eq__` 等方法。

### 4.2 dataclass 自动帮我们做了什么？

| 自动生成的方法 | 作用                      | 没有它会怎样                       |
| -------------- | ------------------------- | ---------------------------------- |
| `__init__`     | 创建对象时初始化字段      | 你得手写 `def __init__(self, ...)` |
| `__repr__`     | `print(obj)` 显示友好信息 | 只显示 `<Student object at 0x...>` |
| `__eq__`       | 用 `==` 比较两个对象      | 比较的是内存地址，永远不相等       |

### 4.3 基础用法：带默认值

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    score: float = 0.0       # 有默认值的字段必须放在没有默认值的字段后面

    def is_passed(self):
        """dataclass 里也能写普通方法"""
        return self.score >= 60

s1 = Student("小明", 18, 88.5)
s2 = Student("小红", 17)      # score 使用默认值 0.0

print(s1)                     # Student(name='小明', age=18, score=88.5)
print(s1.is_passed())         # True
print(s2.is_passed())         # False
```

### 4.4 可变默认值 —— 用 field(default_factory=...)

```python
from dataclasses import dataclass, field

# ❌ 错误写法：直接用 list 作为默认值
# @dataclass
# class ClassRoom:
#     students: list = []        # 所有实例会共享同一个列表！这是 Python 的经典坑

# ✅ 正确写法：用 field(default_factory=list)
@dataclass
class ClassRoom:
    name: str
    students: list = field(default_factory=list)   # 每个实例创建一个新列表

    def add_student(self, student_name):
        self.students.append(student_name)

room1 = ClassRoom("三年二班")
room1.add_student("小明")
room1.add_student("小红")

room2 = ClassRoom("四年一班")
room2.add_student("小刚")

print(room1.students)    # ['小明', '小红']   ← 只有 room1 的学生
print(room2.students)    # ['小刚']           ← 只有 room2 的学生
```

> **记忆技巧**：`default_factory=list` 就是"每次创建新对象时，调用 `list()` 生成一个新列表"。同理，`default_factory=dict` 就是生成一个新字典。

### 4.5 实战案例：商品购物车

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    """商品"""
    name: str
    price: float
    quantity: int = 1

    @property
    def total(self):
        """小计金额"""
        return self.price * self.quantity

@dataclass
class ShoppingCart:
    """购物车"""
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
```

### 4.6 dataclass 的继承

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

@dataclass
class Employee(Person):       # 继承 Person
    department: str
    salary: float = 0.0

e = Employee("小明", 25, "技术部", 15000)
print(e)    # Employee(name='小明', age=25, department='技术部', salary=15000)
```

### 4.7 什么时候用 dataclass？什么时候用普通 class？

| 场景                                     | 推荐          | 原因                                 |
| ---------------------------------------- | ------------- | ------------------------------------ |
| 主要用来**存数据**（如学生、商品、订单） | ✅ dataclass   | 字段多，自动生成代码省事             |
| 有很多**复杂方法**和**内部状态**         | 普通类        | dataclass 更适合数据容器             |
| 需要用 `__add__`、`__len__` 等魔术方法   | 普通类        | dataclass 主要生成 init/repr/eq      |
| 数据需要**验证**或**转换**               | 考虑 Pydantic | Pydantic 在 dataclass 基础上加了验证 |

> **简单原则**：如果一个类"主要是装数据的"，用 dataclass 就对了！

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

| 概念            | 说明             | 示例                        |
| --------------- | ---------------- | --------------------------- |
| `class`         | 定义类           | `class Dog:`                |
| `__init__`      | 初始化方法       | `def __init__(self, name):` |
| `self`          | 实例自身         | `self.name = name`          |
| 继承            | 子类继承父类     | `class Cat(Animal):`        |
| `super()`       | 调用父类方法     | `super().__init__()`        |
| `@dataclass`    | 自动生成样板代码 | `@dataclass class Student:` |
| `__str__`       | print 显示       | `def __str__(self):`        |
| `__add__`       | + 运算           | `def __add__(self, other):` |
| `@property`     | 方法变属性       | `c.area` 不用括号           |
| `@staticmethod` | 静态方法         | 不需要 self                 |
| `@classmethod`  | 类方法           | 第一个参数是 cls            |

---

## 下一步

进入 [第 10 章：错误处理与调试](../10-error-handling/README.md)。
