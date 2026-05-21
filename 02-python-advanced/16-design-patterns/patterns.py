# 第 16 章配套代码：设计模式
# 运行方式：python patterns.py

from dataclasses import dataclass
from typing import Callable

# ============================
# 1. 单例模式
# ============================
print("=== 单例模式 ===")
class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
            print("  创建数据库实例")
        return cls._instance
    def connect(self):
        if not self.connected:
            self.connected = True
            return "连接成功"
        return "已连接"

db1 = Database()
db2 = Database()
print(f"  db1 is db2: {db1 is db2}")
print(f"  {db1.connect()}")
print(f"  {db2.connect()}")

# ============================
# 2. 工厂模式
# ============================
print("\n=== 工厂模式 ===")
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
    pets = {"dog": Dog, "cat": Cat}
    pet_class = pets.get(pet_type)
    if pet_class is None:
        raise ValueError(f"未知类型: {pet_type}")
    return pet_class(name)

dog = create_pet("dog", "旺财")
cat = create_pet("cat", "咪咪")
print(f"  {dog.speak()}")
print(f"  {cat.speak()}")

# ============================
# 3. 策略模式
# ============================
print("\n=== 策略模式 ===")
@dataclass
class Student:
    name: str
    scores: list
    def average(self, strategy: Callable):
        return strategy(self.scores)

def mean(scores):
    return sum(scores) / len(scores)

def trimmed_mean(scores):
    s = sorted(scores)
    return sum(s[1:-1]) / len(s[1:-1])

s = Student("小明", [70, 80, 90, 85, 95])
print(f"  普通平均: {s.average(mean):.1f}")
print(f"  去极值: {s.average(trimmed_mean):.1f}")

# ============================
# 4. 观察者模式
# ============================
print("\n=== 观察者模式 ===")
class EventEmitter:
    def __init__(self):
        self._listeners = {}
    def on(self, event, callback):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    def emit(self, event, *args):
        for cb in self._listeners.get(event, []):
            cb(*args)

emitter = EventEmitter()
emitter.on("login", lambda name: print(f"  欢迎 {name}"))
emitter.on("login", lambda name: print(f"  日志: {name} 登录"))
emitter.on("logout", lambda name: print(f"  {name} 退出"))

print("  触发 login:")
emitter.emit("login", "小明")
print("  触发 logout:")
emitter.emit("logout", "小明")
