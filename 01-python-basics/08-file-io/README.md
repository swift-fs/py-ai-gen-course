# 第 8 章：文件 I/O

> **学习目标**：学会读写文件——文本文件、JSON 文件、CSV 文件，以及 pathlib 的文件操作。

---

## 1. 基本文件读写

### 写入文件

```python
# open(文件名, 模式) → 打开文件
# 模式：'w' 写入（覆盖）、'a' 追加、'r' 读取
# with 语句：自动关闭文件（推荐）

# 写入（覆盖）
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# 追加
with open("hello.txt", "a", encoding="utf-8") as f:
    f.write("第三行（追加）\n")
```

> **为什么要用 `with`？** `with` 会在代码块结束后自动关闭文件，即使发生错误也不会忘记关闭。

### 读取文件

```python
# 读取全部内容
with open("hello.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 逐行读取（推荐，适合大文件）
with open("hello.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())    # strip() 去掉末尾的换行符

# 读取所有行到列表
with open("hello.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(lines)    # ['第一行\n', '第二行\n', '第三行（追加）\n']

# 只读一行
with open("hello.txt", "r", encoding="utf-8") as f:
    first = f.readline()
    print(first)
```

> ⚠️ **始终指定 `encoding="utf-8"`**，否则 Windows 上可能用 GBK 编码，导致中文乱码。

---

## 2. 文件模式

| 模式 | 说明 | 文件不存在时 |
|------|------|-------------|
| `'r'` | 只读（默认） | 报错 |
| `'w'` | 写入（覆盖） | 创建新文件 |
| `'a'` | 追加 | 创建新文件 |
| `'x'` | 独占创建 | 已存在则报错 |
| `'r+'` | 读写 | 报错 |
| `'rb'` | 二进制读 | 报错 |
| `'wb'` | 二进制写 | 创建新文件 |

---

## 3. pathlib —— 更现代的文件操作

`pathlib` 是 Python 推荐的路径和文件操作方式：

```python
from pathlib import Path

# 路径拼接
file = Path("data") / "hello.txt"
print(file)    # data\hello.txt（自动处理不同操作系统的路径分隔符）

# 读写文本（一行搞定！）
file.parent.mkdir(exist_ok=True)   # 创建目录（不存在则创建）
file.write_text("你好，pathlib！\n第二行\n", encoding="utf-8")

content = file.read_text(encoding="utf-8")
print(content)

# 文件信息
print(f"文件名: {file.name}")          # hello.txt
print(f"后缀: {file.suffix}")          # .txt
print(f"父目录: {file.parent}")         # data
print(f"是否存在: {file.exists()}")     # True
print(f"是否是文件: {file.is_file()}")   # True
print(f"大小: {file.stat().st_size} 字节")

# 列出目录下的所有文件
for item in Path(".").iterdir():
    print(f"  {item.name}")
```

### 查找文件

```python
# glob 模式匹配
for py_file in Path(".").rglob("*.py"):
    print(py_file)

# rglob 递归搜索所有子目录
```

---

## 4. JSON 文件

JSON 是最常用的数据存储格式，适合保存配置、结构化数据：

```python
import json
from pathlib import Path

# Python 数据
students = [
    {"name": "小明", "age": 18, "scores": [95, 88]},
    {"name": "小红", "age": 17, "scores": [92, 96]},
]

# 写入 JSON 文件
Path("students.json").write_text(
    json.dumps(students, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# 读取 JSON 文件
text = Path("students.json").read_text(encoding="utf-8")
loaded = json.loads(text)

for s in loaded:
    print(f"{s['name']}: {s['scores']}")
```

### json.dumps vs json.dump

```python
# dumps() → 字符串
text = json.dumps(data, ensure_ascii=False)

# dump() → 直接写入文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# loads() → 从字符串解析
data = json.loads(text)

# load() → 直接从文件读取
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

---

## 5. CSV 文件

CSV（逗号分隔值）是表格数据的常见格式：

```python
import csv

# 写入 CSV
with open("grades.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "数学", "语文"])
    writer.writerow(["小明", 88, 92])
    writer.writerow(["小红", 95, 85])

# 读取 CSV
with open("grades.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)    # ['姓名', '数学', '语文']

# 用字典方式读写（更方便）
with open("grades.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['姓名']}: 数学{row['数学']}, 语文{row['语文']}")
```

---

## 6. 常见陷阱

### 编码问题

```python
# ❌ Windows 默认可能用 GBK
# with open("file.txt", "r") as f:     # 可能 UnicodeDecodeError

# ✅ 始终指定编码
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 忘记关闭文件

```python
# ❌ 不用 with（可能忘记关闭）
f = open("file.txt", "r")
content = f.read()
# 如果这里出错了，文件就不会被关闭
f.close()

# ✅ 使用 with（自动关闭）
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 覆盖文件

```python
# 'w' 模式会清空文件再写！
# 如果想追加，用 'a' 模式
```

---

## 本章小结

| 方法 | 说明 |
|------|------|
| `open()` + `with` | 标准文件读写 |
| `f.read()` | 读取全部 |
| `f.readline()` | 读取一行 |
| `f.readlines()` | 读取所有行到列表 |
| `f.write()` | 写入字符串 |
| `Path.read_text()` | pathlib 一行读取 |
| `Path.write_text()` | pathlib 一行写入 |
| `json.dumps/loads` | JSON 序列化/反序列化 |
| `json.dump/load` | JSON 文件读写 |
| `csv.reader/writer` | CSV 读写 |

---

## 下一步

恭喜你完成了**入门篇**！现在进入 [第 9 章：面向对象编程](../../02-python-advanced/09-oop/README.md)，开始进阶之旅。
