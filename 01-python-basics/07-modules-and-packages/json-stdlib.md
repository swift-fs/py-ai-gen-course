# json 标准库 —— JSON 数据处理

> **学习目标**：掌握 `json` 模块的核心功能，能在 Python 对象和 JSON 之间互相转换，处理文件读写，并了解常见的序列化陷阱。

---

## 1. 什么是 JSON？

**JSON**（JavaScript Object Notation）是一种轻量级的数据交换格式。它长得像这样：

```json
{
  "name": "小明",
  "age": 25,
  "hobbies": ["编程", "阅读", "游泳"],
  "address": {
    "city": "北京",
    "district": "海淀"
  },
  "is_student": false
}
```

### 为什么学 JSON？

JSON 是当今最流行的数据交换格式，几乎无处不在：

- **Web API**：前后端数据交互几乎都用 JSON
- **配置文件**：很多工具和框架使用 JSON 作为配置格式
- **数据存储**：NoSQL 数据库（如 MongoDB）使用 JSON 格式
- **日志**：结构化日志常用 JSON 格式

---

## 2. 什么是 json 模块？

`json` 是 Python 标准库中处理 JSON 数据的模块，提供了两个核心功能：

| 功能         | Python 对象 → JSON     | JSON → Python 对象     |
| ------------ | ---------------------- | ---------------------- |
| **字符串**   | `json.dumps()`         | `json.loads()`         |
| **文件**     | `json.dump()`          | `json.load()`          |

> **记忆技巧**：带 `s` 的（`dumps`/`loads`）操作字符串（**s**tring），不带的操作文件。

```python
import json
```

---

## 3. Python 与 JSON 的类型对应

JSON 和 Python 的数据类型并不完全一一对应：

| JSON        | Python          | 说明               |
| ----------- | --------------- | ------------------ |
| object      | `dict`          | 键值对             |
| array       | `list`          | 数组               |
| string      | `str`           | 字符串             |
| number(整数) | `int`          | 整数               |
| number(浮点) | `float`        | 浮点数             |
| `true`      | `True`          | 布尔值             |
| `false`     | `False`         | 布尔值             |
| `null`      | `None`          | 空值               |

**注意以下区别**：
- JSON 中只有 `true/false/null`，Python 中是 `True/False/None`
- JSON 的键（key）**必须是双引号字符串**，Python 的字典键可以是任何不可变类型
- JSON 不支持 Python 的 `tuple`、`set`、复数等类型

---

## 4. json.dumps() —— Python 对象 → JSON 字符串

### 基本用法

```python
import json

data = {
    "name": "小明",
    "age": 25,
    "hobbies": ["编程", "阅读"],
    "is_student": False,
    "score": None
}

# 转换为 JSON 字符串
json_str = json.dumps(data)
print(json_str)
# {"name": "\u5c0f\u660e", "age": 25, "hobbies": ["\u7f16\u7a0b", "\u9605\u8bfb"], ...}
```

> 你会发现中文变成了 `\u5c0f\u660e` 这样的 Unicode 转义序列。这是因为默认 `ensure_ascii=True`。

### 常用参数

#### `ensure_ascii=False` —— 保留中文

```python
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)
# {"name": "小明", "age": 25, "hobbies": ["编程", "阅读"], ...}
```

> **建议**：处理中文时始终加上 `ensure_ascii=False`。

#### `indent` —— 美化格式

```python
# 缩进 2 个空格
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)
```

输出：

```json
{
  "name": "小明",
  "age": 25,
  "hobbies": [
    "编程",
    "阅读"
  ],
  "is_student": false,
  "score": null
}
```

#### `sort_keys=True` —— 按键名排序

```python
json_str = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
# 输出的 JSON 会按照 key 的字母顺序排列
```

#### `separators` —— 紧凑格式

```python
# 最紧凑的格式（去掉多余空格）
compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
print(compact)
# {"name":"小明","age":25,"hobbies":["编程","阅读"],"is_student":false,"score":null}
```

---

## 5. json.loads() —— JSON 字符串 → Python 对象

### 基本用法

```python
import json

json_str = '{"name": "小明", "age": 25, "hobbies": ["编程", "阅读"]}'

# 解析 JSON 字符串
data = json.loads(json_str)
print(type(data))        # <class 'dict'>
print(data["name"])      # 小明
print(data["hobbies"])   # ['编程', '阅读']
print(data["hobbies"][0])  # 编程
```

### 从不同来源解析

```python
# 解析数组
json_array = '[1, 2, 3, "hello"]'
result = json.loads(json_array)
print(result)  # [1, 2, 3, 'hello']
print(type(result))  # <class 'list'>

# 解析嵌套结构
nested = '{"user": {"name": "小明", "scores": [95, 88, 92]}}'
data = json.loads(nested)
print(data["user"]["scores"][0])  # 95
```

### 常见解析错误

```python
# 错误 1：JSON 键必须用双引号
# json.loads("{'name': '小明'}")  # ❌ 报错！单引号不是合法 JSON
json.loads('{"name": "小明"}')    # ✅ 正确

# 错误 2：末尾不能有多余的逗号
# json.loads('{"name": "小明",}')  # ❌ 报错！
json.loads('{"name": "小明"}')     # ✅ 正确

# 错误 3：不是有效的 JSON
# json.loads("hello")  # ❌ 报错！
```

> **提示**：如果不确定 JSON 字符串是否合法，可以用在线 JSON 校验工具（如 jsonlint.com）检查。

---

## 6. json.dump() / json.load() —— 直接读写文件

### 写入 JSON 文件

```python
import json

data = {
    "name": "小明",
    "age": 25,
    "hobbies": ["编程", "阅读", "游泳"]
}

# 写入 JSON 文件
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
```

> **注意**：`json.dump()` 没有 `s`，第一个参数是 Python 对象，第二个参数是文件对象。

### 读取 JSON 文件

```python
import json

# 读取 JSON 文件
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data["name"])    # 小明
print(data["hobbies"])  # ['编程', '阅读', '游泳']
```

> **提示**：读写文件时始终指定 `encoding="utf-8"`，特别是在 Windows 上。

### `dumps` vs `dump` 对比

| 函数          | 输入          | 输出       | 使用场景                 |
| ------------- | ------------- | ---------- | ------------------------ |
| `json.dumps()` | Python 对象  | 字符串     | API 响应、日志、内存处理 |
| `json.dump()`  | Python 对象  | 文件       | 保存到文件               |
| `json.loads()` | JSON 字符串  | Python 对象 | 解析字符串、API 请求     |
| `json.load()`  | JSON 文件    | Python 对象 | 从文件读取               |

---

## 7. 完整读写流程示例

```python
import json
from pathlib import Path

# 要保存的数据
students = [
    {"name": "小明", "age": 20, "scores": {"math": 95, "english": 88}},
    {"name": "小红", "age": 21, "scores": {"math": 92, "english": 96}},
    {"name": "小华", "age": 20, "scores": {"math": 88, "english": 90}},
]

file_path = Path("students.json")

# 1. 写入 JSON 文件
with file_path.open("w", encoding="utf-8") as file:
    json.dump(students, file, ensure_ascii=False, indent=2)
print(f"已保存 {len(students)} 条记录到 {file_path}")

# 2. 读取 JSON 文件
with file_path.open("r", encoding="utf-8") as file:
    loaded = json.load(file)

# 3. 处理数据
for student in loaded:
    avg = sum(student["scores"].values()) / len(student["scores"])
    print(f"{student['name']}: 平均分 {avg:.1f}")
```

---

## 8. 序列化陷阱与解决方案

### 陷阱 1：不支持的类型

`json` 只能序列化基本类型。Python 的 `set`、`tuple`（会被转成数组）、`datetime` 等类型不能直接序列化：

```python
import json
from datetime import datetime

data = {"time": datetime.now()}

# json.dumps(data)  # ❌ TypeError: Object of type datetime is not JSON serializable
```

**解决方法**：在序列化前手动转换：

```python
data = {"time": datetime.now().isoformat()}  # ✅ 转为字符串
json_str = json.dumps(data)
```

或者使用 `default` 参数自定义序列化行为：

```python
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"无法序列化 {type(obj)}")

data = {"time": datetime.now()}
json_str = json.dumps(data, default=custom_serializer, ensure_ascii=False)
print(json_str)  # {"time": "2024-06-01T14:30:45.123456"}
```

### 陷阱 2：元组会变成列表

```python
import json

data = {"coordinates": (10, 20)}
json_str = json.dumps(data)
print(json_str)  # {"coordinates": [10, 20]}

# 反序列化后变成了列表
loaded = json.loads(json_str)
print(type(loaded["coordinates"]))  # <class 'list'>，不是 tuple！
```

### 陷阱 3：JSON 键只能是字符串

```python
import json

# Python 允许整数键
data = {1: "one", 2: "two"}
json_str = json.dumps(data)
print(json_str)  # {"1": "one", "2": "two"}（键变成了字符串）

loaded = json.loads(json_str)
print(loaded)  # {'1': 'one', '2': 'two'}（反序列化后键是字符串）
```

### 陷阱 4：浮点数精度

```python
import json

data = {"value": 0.1 + 0.2}
json_str = json.dumps(data)
print(json_str)  # {"value": 0.30000000000000004}
```

这是浮点数的固有问题，不是 `json` 模块的 bug。

---

## 9. 进阶用法

### 自定义解码

使用 `object_hook` 参数自定义 JSON 对象的解析方式：

```python
import json

json_str = '''
[
    {"name": "小明", "age": 20},
    {"name": "小红", "age": 21}
]
'''

# 自定义解析：把每个对象转为元组
def to_tuple(obj):
    return (obj.get("name"), obj.get("age"))

result = json.loads(json_str, object_hook=to_tuple)
print(result)  # [('小明', 20), ('小红', 21)]
```

### 精确控制数值解析

```python
import json
from decimal import Decimal

json_str = '{"price": 19.99, "quantity": 3}'

# 用 Decimal 解析浮点数（避免精度问题）
data = json.loads(json_str, parse_float=Decimal)
print(data["price"])        # Decimal('19.99')
print(type(data["price"]))  # <class 'decimal.Decimal'>
```

### 格式化命令行 JSON 输出

在命令行中快速格式化 JSON（Python 自带工具）：

```powershell
# 格式化 JSON 文件
python -m json.tool data.json

# 从管道输入格式化
echo '{"name":"小明","age":25}' | python -m json.tool
```

---

## 10. 实用示例

### 示例 1：简单的配置管理器

```python
import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.path = Path(config_path)
        self.config = self._load()

    def _load(self):
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save(self):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self.config, file, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()

# 使用
config = ConfigManager()
config.set("theme", "dark")
config.set("language", "zh-CN")
print(f"当前主题: {config.get('theme')}")
print(f"当前语言: {config.get('language')}")
```

### 示例 2：JSON 日志记录

```python
import json
from datetime import datetime
from pathlib import Path

def log_event(level, message, **details):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
        **details
    }

    log_path = Path("app.log")
    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

log_event("INFO", "程序启动", version="1.0.0")
log_event("WARNING", "内存使用率高", usage="85%")
log_event("ERROR", "数据库连接失败", retry_count=3)
```

### 示例 3：合并多个 JSON 文件

```python
import json
from pathlib import Path

def merge_json_files(directory, output_file):
    all_data = []

    for json_file in Path(directory).glob("*.json"):
        with json_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                all_data.extend(data)
            else:
                all_data.append(data)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=2)

    print(f"已合并 {len(all_data)} 条记录到 {output_file}")
```

### 示例 4：模拟 API 响应

```python
import json

def make_api_response(success, data=None, message=""):
    response = {
        "success": success,
        "message": message,
        "data": data
    }
    return json.dumps(response, ensure_ascii=False)

# 成功响应
print(make_api_response(True, {"id": 1, "name": "小明"}, "查询成功"))

# 错误响应
print(make_api_response(False, message="用户不存在"))
```

---

## 11. 常用函数速查表

| 函数                              | 说明                       | 示例                                         |
| --------------------------------- | -------------------------- | -------------------------------------------- |
| `json.dumps(obj)`                 | Python → JSON 字符串       | `json.dumps({"a": 1})`                       |
| `json.loads(s)`                   | JSON 字符串 → Python       | `json.loads('{"a": 1}')`                     |
| `json.dump(obj, fp)`              | Python → JSON 文件         | `json.dump(data, file)`                      |
| `json.load(fp)`                   | JSON 文件 → Python         | `json.load(file)`                            |
| `ensure_ascii=False`              | 保留非 ASCII 字符（中文） | `json.dumps(data, ensure_ascii=False)`       |
| `indent=2`                        | 美化缩进                  | `json.dumps(data, indent=2)`                 |
| `sort_keys=True`                  | 按键名排序                | `json.dumps(data, sort_keys=True)`           |
| `default=func`                    | 自定义序列化              | `json.dumps(data, default=custom_serializer)` |

---

## 12. 常见问题

### Q：JSON 字符串用单引号还是双引号？

JSON 标准要求**键和字符串值都必须用双引号**。单引号不是合法的 JSON：

```python
# ❌ 不是合法 JSON
# '{"name": "小明"}'  ← 虽然这在 Python 中是字符串，但如果里面也用单引号就不行

# ✅ 合法 JSON
'{"name": "小明"}'   ← 外面用 Python 的单引号，里面用 JSON 的双引号
```

### Q：JSON 文件编码问题怎么解决？

始终在 `open()` 中指定 `encoding="utf-8"`：

```python
# ✅ 推荐
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
```

### Q：怎么验证 JSON 格式是否正确？

```python
import json

def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError as error:
        print(f"JSON 格式错误: {error}")
        return False

print(is_valid_json('{"name": "小明"}'))  # True
print(is_valid_json("{'name': '小明'}"))  # False
```

### Q：需要更快的 JSON 性能怎么办？

标准库的 `json` 性能已经不错。如果需要更高性能，可以使用第三方库：

- **`orjson`**：最快的 JSON 库之一，支持更多类型
- **`ujson`**：比标准库快 2-3 倍
- **`msgspec`**：同时支持 JSON 和 MessagePack，性能极佳

---

## 返回

[← 返回模块与包](./README.md)
