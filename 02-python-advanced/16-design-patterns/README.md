# 第 16 章：设计模式

> **学习目标**：用 Pythonic 的方式实现常用设计模式——单例、工厂、策略、观察者。

---

## 1. 单例模式

确保一个类只有一个实例：

```python
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
        return cls._instance

    def connect(self):
        if not self.connected:
            print("连接数据库")
            self.connected = True

db1 = Database()
db2 = Database()
print(db1 is db2)    # True（同一个实例）
```

---

## 2. 工厂模式

用函数或方法创建对象，而不是直接调用构造函数：

```python
from dataclasses import dataclass

@dataclass
class Dog:
    name: str
    def speak(self):
        return f"{self.name}: 汪汪！"

@dataclass
class Cat:
    name: str
    def speak(self):
        return f"{self.name}: 喵喵！"

def create_pet(pet_type, name):
    """工厂函数：根据类型创建对象"""
    pets = {"dog": Dog, "cat": Cat}
    pet_class = pets.get(pet_type)
    if pet_class is None:
        raise ValueError(f"未知宠物类型: {pet_type}")
    return pet_class(name)

dog = create_pet("dog", "旺财")
cat = create_pet("cat", "咪咪")
print(dog.speak())    # 旺财: 汪汪！
print(cat.speak())    # 咪咪: 喵喵！
```

---

## 3. 策略模式

定义一系列算法，封装后可以互换：

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class Student:
    name: str
    scores: list

    def average(self, strategy: Callable[[list], float]):
        """使用不同的计算策略"""
        return strategy(self.scores)

# 策略1：普通平均分
def mean(scores):
    return sum(scores) / len(scores)

# 策略2：去掉最高最低后的平均分
def trimmed_mean(scores):
    sorted_scores = sorted(scores)
    return sum(sorted_scores[1:-1]) / len(sorted_scores[1:-1])

# 策略3：加权平均（后面的分数权重更大）
def weighted(scores):
    weights = [i + 1 for i in range(len(scores))]
    return sum(s * w for s, w in zip(scores, weights)) / sum(weights)

s = Student("小明", [70, 80, 90, 85, 95])
print(f"普通平均: {s.average(mean):.1f}")
print(f"去极值平均: {s.average(trimmed_mean):.1f}")
print(f"加权平均: {s.average(weighted):.1f}")
```

---

## 4. 观察者模式

当一个对象状态变化时，通知所有订阅者：

```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        """订阅事件"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def emit(self, event, *args, **kwargs):
        """触发事件"""
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

# 使用
emitter = EventEmitter()

emitter.on("login", lambda name: print(f"  欢迎 {name}"))
emitter.on("login", lambda name: print(f"  记录日志: {name} 登录"))
emitter.on("logout", lambda name: print(f"  {name} 已退出"))

print("触发 login:")
emitter.emit("login", "小明")

print("触发 logout:")
emitter.emit("logout", "小明")
```

---

## 本章小结

| 模式 | 用途 | Pythonic 实现 |
|------|------|-------------|
| 单例 | 全局唯一实例 | `__new__` 或模块级变量 |
| 工厂 | 按条件创建对象 | 工厂函数/字典映射 |
| 策略 | 算法可互换 | 函数作为参数 |
| 观察者 | 事件通知 | 回调函数/事件系统 |

---

## 下一步

进入 [第 17 章：测试](../17-testing/README.md)。
