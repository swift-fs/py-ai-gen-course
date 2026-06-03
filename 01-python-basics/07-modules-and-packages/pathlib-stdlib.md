# pathlib 标准库 —— 路径操作

> **学习目标**：掌握 `pathlib` 模块中 `Path` 类的核心用法，能优雅地完成路径拼接、文件检查、读写文件、目录遍历等常见文件系统操作。

---

## 1. 什么是 pathlib 模块？

`pathlib` 是 Python 3.4 引入的面向对象的路径操作模块。它用 `Path` 对象来表示文件系统路径，比传统的字符串拼接更安全、更优雅。

### 为什么用 pathlib 而不是 `os.path`？

```python
# 传统方式（os.path）—— 字符串拼接，容易出错
import os
config_path = os.path.join(os.getcwd(), "config", "settings.json")

# pathlib 方式 —— 面向对象，更直观
from pathlib import Path
config_path = Path.cwd() / "config" / "settings.json"
```

| 对比项     | `os.path`            | `pathlib`                  |
| ---------- | -------------------- | -------------------------- |
| 风格       | 函数式，字符串拼接   | 面向对象，路径运算符 `/`   |
| 跨平台     | 需要手动 `join`      | `/` 自动处理分隔符         |
| 可读性     | 一般                 | 很好                       |
| 功能       | 基本够用             | 更丰富                     |

> **建议**：新项目优先使用 `pathlib`，它已经是 Python 官方推荐的路径操作方式。

---

## 2. 导入与创建路径

```python
from pathlib import Path
```

### 创建 Path 对象的几种方式

```python
# 方式 1：直接传入路径字符串
p1 = Path("config/settings.json")
print(p1)  # config/settings.json

# 方式 2：使用当前工作目录
cwd = Path.cwd()
print(f"当前目录: {cwd}")

# 方式 3：使用用户主目录
home = Path.home()
print(f"主目录: {home}")

# 方式 4：从 __file__ 获取当前脚本路径
# script = Path(__file__)       # 当前脚本文件
# script_dir = script.parent    # 当前脚本所在目录
```

### Windows 和 Mac/Linux 的区别

`pathlib` 会根据操作系统自动选择正确的路径风格：

```python
# 在 Windows 上
Path("data/file.txt")  # 显示为 data\file.txt（反斜杠）

# 在 Mac/Linux 上
Path("data/file.txt")  # 显示为 data/file.txt（正斜杠）
```

你不需要关心斜杠方向，`pathlib` 帮你处理好了。

---

## 3. 路径拼接

### 使用 `/` 运算符拼接路径

这是 `pathlib` 最大的亮点——用 `/` 拼接路径，就像写路径本身一样自然：

```python
base = Path("/home/user")
config = base / "config" / "settings.json"
print(config)  # /home/user/config/settings.json

# 也可以混合字符串和 Path 对象
data = Path("data")
file_path = data / "reports" / "2024" / "report.csv"
print(file_path)  # data/reports/2024/report.csv
```

> **注意**：`/` 的第一个操作数必须有一个是 `Path` 对象，不能是两个纯字符串。

### `joinpath()` 方法

如果不喜欢 `/` 运算符，也可以用 `joinpath()`：

```python
p = Path("/home/user").joinpath("docs", "report.pdf")
print(p)  # /home/user/docs/report.pdf
```

---

## 4. 路径的各个部分

`Path` 对象可以方便地拆分出路径的各个部分：

```python
p = Path("/home/user/docs/report.pdf")

print(f"完整路径: {p}")           # /home/user/docs/report.pdf
print(f"父目录: {p.parent}")      # /home/user/docs
print(f"父目录的父目录: {p.parent.parent}")  # /home/user
print(f"文件名: {p.name}")        # report.pdf
print(f"文件名(无后缀): {p.stem}")  # report
print(f"后缀: {p.suffix}")        # .pdf
print(f"所有后缀: {p.suffixes}")   # ['.pdf']
```

### 多后缀的文件

```python
p = Path("archive.tar.gz")

print(f"文件名: {p.name}")       # archive.tar.gz
print(f"stem: {p.stem}")         # archive.tar
print(f"suffix: {p.suffix}")     # .gz
print(f"suffixes: {p.suffixes}") # ['.tar', '.gz']
```

### 路径的各个组成部分

```python
p = Path("/home/user/docs/report.pdf")

print(f"盘符/根: {p.anchor}")    # /（Linux）或 C:\（Windows）
print(f"所有部分: {p.parts}")    # ('/', 'home', 'user', 'docs', 'report.pdf')
```

### 修改路径的部分

```python
p = Path("report.pdf")

# 修改文件名
new_name = p.with_name("summary.pdf")
print(new_name)  # summary.pdf

# 修改后缀
new_suffix = p.with_suffix(".txt")
print(new_suffix)  # report.txt

# 修改 stem（文件名主体）
new_stem = p.with_stem("final_report")
print(new_stem)  # final_report.pdf（Python 3.9+）
```

---

## 5. 路径检查

### 是否存在

```python
p = Path("some_file.txt")

if p.exists():
    print("路径存在")
else:
    print("路径不存在")
```

### 是文件还是目录

```python
p = Path("README.md")

print(p.is_file())  # True（是文件）
print(p.is_dir())   # False（不是目录）

d = Path(".")
print(d.is_dir())   # True（是目录）
print(d.is_file())  # False
```

### 其他检查

```python
p = Path("some_script.sh")

print(p.is_absolute())  # 是否是绝对路径
print(p.is_relative_to("/home"))  # 是否相对于某个路径（Python 3.9+）
```

### 获取文件信息

```python
p = Path("README.md")

# 文件大小（字节）
print(f"大小: {p.stat().st_size} 字节")

# 修改时间
import datetime
modified = datetime.datetime.fromtimestamp(p.stat().st_mtime)
print(f"修改时间: {modified}")
```

---

## 6. 文件读写

`Path` 对象自带读写方法，比 `open()` 更简洁。

### `read_text()` / `write_text()` —— 文本文件

```python
from pathlib import Path

file_path = Path("greeting.txt")

# 写入文本文件（覆盖写入）
file_path.write_text("你好，世界！\n第二行内容\n", encoding="utf-8")

# 读取整个文本文件
content = file_path.read_text(encoding="utf-8")
print(content)
```

> **注意**：
> - `write_text()` 是**覆盖写入**，不是追加。如果需要追加，请用 `open()` 的 `"a"` 模式。
> - 在 Windows 上建议始终指定 `encoding="utf-8"`，避免编码问题。

### `read_bytes()` / `write_bytes()` —— 二进制文件

```python
from pathlib import Path

# 读取二进制文件（如图片）
img_path = Path("photo.jpg")
data = img_path.read_bytes()
print(f"图片大小: {len(data)} 字节")

# 写入二进制文件
backup_path = Path("photo_backup.jpg")
backup_path.write_bytes(data)
```

### 使用 `open()` 方法

对于更复杂的读写需求（如追加、逐行读取），可以用 `open()` 方法：

```python
from pathlib import Path

file_path = Path("log.txt")

# 追加内容
with file_path.open("a", encoding="utf-8") as file:
    file.write("新的一行日志\n")

# 逐行读取
with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

---

## 7. 目录操作

### 创建目录

```python
from pathlib import Path

# 创建单层目录（如果不存在）
dir_path = Path("output")
dir_path.mkdir(exist_ok=True)  # exist_ok=True：已存在时不报错

# 创建多层目录
deep_dir = Path("output/reports/2024")
deep_dir.mkdir(parents=True, exist_ok=True)
# parents=True：自动创建所有中间目录
# exist_ok=True：已存在时不报错
```

> **推荐**：始终加上 `parents=True, exist_ok=True` 参数，这样目录已存在时不会报错，非常省心。

### 删除文件和目录

```python
from pathlib import Path

# 删除文件
file_path = Path("temp.txt")
file_path.unlink(missing_ok=True)  # missing_ok=True：不存在时不报错

# 删除空目录
dir_path = Path("empty_dir")
dir_path.rmdir()  # 目录必须为空，否则报错
```

> **注意**：`pathlib` 没有直接删除非空目录的方法。如果需要递归删除整个目录树，使用 `shutil.rmtree()`：

```python
import shutil
shutil.rmtree("output")  # 删除整个 output 目录及其内容
```

### 重命名/移动

```python
from pathlib import Path

# 重命名文件
old_path = Path("old_name.txt")
new_path = Path("new_name.txt")
old_path.rename(new_path)

# 移动文件到其他目录
src = Path("report.pdf")
dst = Path("archive/report.pdf")
dst.parent.mkdir(parents=True, exist_ok=True)
src.rename(dst)
```

---

## 8. 查找文件（glob 模式匹配）

### `glob()` —— 匹配当前目录

```python
from pathlib import Path

# 查找当前目录下所有 .txt 文件
for txt_file in Path(".").glob("*.txt"):
    print(txt_file)

# 查找 src 目录下所有 Python 文件
for py_file in Path("src").glob("*.py"):
    print(py_file)
```

### `rglob()` —— 递归匹配（包含所有子目录）

```python
from pathlib import Path

# 递归查找所有 .py 文件
for py_file in Path(".").rglob("*.py"):
    print(py_file)

# 等价于：
for py_file in Path(".").glob("**/*.py"):
    print(py_file)
```

### glob 模式语法

| 模式    | 说明                   | 示例              |
| ------- | ---------------------- | ----------------- |
| `*`     | 匹配任意多个字符       | `*.txt`           |
| `?`     | 匹配单个字符           | `file?.txt`       |
| `[abc]` | 匹配方括号中的任一字符 | `file[123].txt`   |
| `**`    | 递归匹配所有子目录     | `**/*.py`         |

### 实用的查找示例

```python
from pathlib import Path

# 找出所有图片文件
image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
for file_path in Path("photos").rglob("*"):
    if file_path.is_file() and file_path.suffix.lower() in image_extensions:
        print(f"找到图片: {file_path}")

# 找出大于 1MB 的文件
for file_path in Path(".").rglob("*"):
    if file_path.is_file() and file_path.stat().st_size > 1024 * 1024:
        size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"大文件: {file_path} ({size_mb:.1f} MB)")
```

---

## 9. 路径转换

### 转为绝对路径

```python
from pathlib import Path

relative = Path("data/file.txt")
absolute = relative.resolve()
print(f"相对路径: {relative}")
print(f"绝对路径: {absolute}")
```

### 转为字符串

```python
from pathlib import Path

p = Path("data/file.txt")
print(str(p))       # 'data/file.txt'（字符串形式）
print(p.as_posix()) # 'data/file.txt'（始终用正斜杠，跨平台时有用）
```

### 相对路径计算

```python
from pathlib import Path

base = Path("/home/user/project")
target = Path("/home/user/project/src/main.py")

# 计算相对路径
rel = target.relative_to(base)
print(rel)  # src/main.py
```

---

## 10. 实用示例

### 示例 1：安全地读写配置文件

```python
from pathlib import Path
import json

config_path = Path("config.json")

# 默认配置
default_config = {"theme": "dark", "language": "zh-CN", "font_size": 14}

# 如果配置文件不存在，创建默认配置
if not config_path.exists():
    config_path.write_text(json.dumps(default_config, ensure_ascii=False, indent=2), encoding="utf-8")
    print("已创建默认配置文件")

# 读取配置
config_text = config_path.read_text(encoding="utf-8")
config = json.loads(config_text)
print(f"当前配置: {config}")
```

### 示例 2：整理下载文件夹

```python
from pathlib import Path

def organize_downloads(download_dir):
    download_path = Path(download_dir)

    # 按扩展名分类
    categories = {
        "图片": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
        "文档": {".pdf", ".doc", ".docx", ".txt", ".xlsx"},
        "视频": {".mp4", ".avi", ".mkv", ".mov"},
        "音乐": {".mp3", ".wav", ".flac"},
        "压缩包": {".zip", ".rar", ".7z", ".tar.gz"},
    }

    for file_path in download_path.iterdir():
        if not file_path.is_file():
            continue

        # 找到对应的分类
        suffix = file_path.suffix.lower()
        category = "其他"
        for cat, extensions in categories.items():
            if suffix in extensions:
                category = cat
                break

        # 移动文件
        target_dir = download_path / category
        target_dir.mkdir(exist_ok=True)
        target_path = target_dir / file_path.name

        if not target_path.exists():
            file_path.rename(target_path)
            print(f"移动: {file_path.name} → {category}/")

# organize_downloads("C:/Users/你的用户名/Downloads")
```

### 示例 3：批量重命名文件

```python
from pathlib import Path

def batch_rename(directory, old_suffix, new_suffix):
    dir_path = Path(directory)

    for file_path in dir_path.glob(f"*{old_suffix}"):
        new_path = file_path.with_suffix(new_suffix)
        file_path.rename(new_path)
        print(f"重命名: {file_path.name} → {new_path.name}")

# 把所有 .jpeg 改成 .jpg
# batch_rename("photos", ".jpeg", ".jpg")
```

### 示例 4：统计目录下的文件类型

```python
from pathlib import Path
from collections import Counter

def count_file_types(directory):
    dir_path = Path(directory)
    extensions = []

    for file_path in dir_path.rglob("*"):
        if file_path.is_file():
            ext = file_path.suffix.lower() if file_path.suffix else "(无后缀)"
            extensions.append(ext)

    counter = Counter(extensions)
    print("文件类型统计:")
    for ext, count in counter.most_common(10):
        print(f"  {ext}: {count} 个文件")

count_file_types(".")
```

---

## 11. 常用方法速查表

| 方法 / 属性             | 说明                         | 示例                          |
| ----------------------- | ---------------------------- | ----------------------------- |
| `Path.cwd()`            | 当前工作目录                 | `Path.cwd()`                  |
| `Path.home()`           | 用户主目录                   | `Path.home()`                 |
| `p / "sub"`             | 路径拼接                     | `Path("a") / "b"`             |
| `p.parent`              | 父目录                       | `Path("a/b/c").parent`        |
| `p.name`                | 文件名（含后缀）             | `Path("a/b.txt").name`        |
| `p.stem`                | 文件名（不含后缀）           | `Path("a/b.txt").stem`        |
| `p.suffix`              | 后缀                         | `Path("a/b.txt").suffix`      |
| `p.exists()`            | 是否存在                     | `Path("a.txt").exists()`      |
| `p.is_file()`           | 是否是文件                   | `Path("a.txt").is_file()`     |
| `p.is_dir()`            | 是否是目录                   | `Path("dir").is_dir()`        |
| `p.mkdir()`             | 创建目录                     | `Path("dir").mkdir()`         |
| `p.unlink()`            | 删除文件                     | `Path("a.txt").unlink()`      |
| `p.rename(target)`      | 重命名/移动                  | `p.rename("new.txt")`         |
| `p.read_text()`         | 读取文本文件                 | `p.read_text(encoding="utf-8")` |
| `p.write_text(s)`       | 写入文本文件                 | `p.write_text("hello")`       |
| `p.read_bytes()`        | 读取二进制文件               | `p.read_bytes()`              |
| `p.write_bytes(b)`      | 写入二进制文件               | `p.write_bytes(data)`         |
| `p.glob(pattern)`       | 匹配当前目录                 | `p.glob("*.py")`              |
| `p.rglob(pattern)`      | 递归匹配                     | `p.rglob("*.py")`             |
| `p.resolve()`           | 转为绝对路径                 | `Path(".").resolve()`         |
| `p.stat()`              | 文件信息（大小、时间等）     | `p.stat().st_size`            |
| `p.iterdir()`           | 遍历目录内容                 | `for f in p.iterdir()`        |

---

## 12. 常见问题

### Q：`pathlib` 和 `os.path` 可以混用吗？

可以，但不推荐。`pathlib` 能覆盖 `os.path` 绝大部分功能。如果确实需要，可以把 `Path` 对象传给 `str()` 转换：

```python
from pathlib import Path
import os

p = Path("some/file.txt")
os.path.getsize(str(p))  # 可以，但 Path 自带 .stat().st_size
```

### Q：`write_text` 编码问题怎么解决？

在 Windows 上，默认编码可能不是 UTF-8。建议始终指定编码：

```python
Path("file.txt").write_text("中文内容", encoding="utf-8")
content = Path("file.txt").read_text(encoding="utf-8")
```

### Q：怎么获取目录下所有文件（不包含子目录）？

```python
from pathlib import Path

files = [f for f in Path(".").iterdir() if f.is_file()]
for f in files:
    print(f.name)
```

### Q：怎么创建临时文件？

`pathlib` 不直接支持临时文件，可以用 `tempfile` 模块：

```python
import tempfile
from pathlib import Path

# 创建临时目录
with tempfile.TemporaryDirectory() as tmp_dir:
    tmp_path = Path(tmp_dir)
    tmp_file = tmp_path / "temp.txt"
    tmp_file.write_text("临时内容", encoding="utf-8")
    print(f"临时文件: {tmp_file}")
    # with 结束后，临时目录和文件会被自动删除
```

---

## 返回

[← 返回模块与包](./README.md)
