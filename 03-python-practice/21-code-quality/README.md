# 第 21 章：代码质量

> **学习目标**：学会使用 ruff 格式化和检查代码，养成写高质量代码的习惯。

---

## 1. ruff —— 代码格式化和检查

ruff 是超快的 Python 代码工具，替代 flake8、isort、black：

### 安装

```powershell
uv add --dev ruff
```

### 常用命令

```powershell
# 检查代码问题
uv run ruff check .

# 自动修复问题
uv run ruff check --fix .

# 格式化代码
uv run ruff format .

# 格式化并检查
uv run ruff format . ; uv run ruff check .
```

### 常见问题

```python
# 未使用的导入
import os          # ❌ ruff 报错：未使用
import sys

# 变量名问题
x = 1              # 可能提示命名不好

# 行过长
very_long_line = "this is a very long line that exceeds the default line length limit of 88 characters"  # ruff 会格式化

# 排序
import sys         # ❌ 应该在 os 前面
import os
```

---

## 2. 代码风格建议

### 命名

```python
# ✅ 好的命名
student_name = "小明"
def calculate_average(scores):
    pass
class UserProfile:
    pass
MAX_RETRIES = 3

# ❌ 不好的命名
sn = "小明"
def calc(s):
    pass
```

### 函数设计

```python
# ✅ 一个函数做一件事
def read_file(path):
    return Path(path).read_text(encoding="utf-8")

def parse_config(text):
    return json.loads(text)

# ❌ 做太多事
def read_and_parse(path):
    # 又读文件又解析
    pass
```

### 类型注解

```python
# ✅ 有类型注解，意图清晰
def search_users(name: str, age_min: int = 0) -> list[dict]:
    pass
```

---

## 3. 项目配置

在 `pyproject.toml` 中配置 ruff：

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I"]    # E: 风格, F: 错误, I: 导入排序
```

---

## 4. 完整工作流

```powershell
# 1. 写代码
# 2. 格式化
uv run ruff format .

# 3. 检查问题
uv run ruff check --fix .

# 4. 运行测试
uv run pytest

# 5. 提交
git add .
git commit -m "feat: 添加新功能"
```

---

## 课程总结

恭喜你完成了整个课程！你学到了：

**入门篇**：变量、数据类型、运算符、字符串、数据结构、控制流、函数、模块、文件 I/O

**进阶篇**：OOP、错误处理、装饰器、生成器、类型注解、异步编程、标准库、设计模式、测试

**实战篇**：项目结构、CLI 应用、Web API、代码质量

继续学习的方向：
- 数据库（SQLAlchemy）
- 前端框架（Gradio、Streamlit）
- 数据科学（pandas、numpy）
- AI/ML 应用开发

---

> 编程是一项实践技能。多写项目、多读优秀代码、多写测试，你会越来越强！
