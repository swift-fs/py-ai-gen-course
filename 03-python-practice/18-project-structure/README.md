# 第 18 章：项目结构与 uv

> **学习目标**：掌握 Python 项目标准结构，学会使用 uv 管理依赖和虚拟环境。

---

## 1. 项目目录规范

一个规范的 Python 项目结构：

```
my-project/
├── pyproject.toml        # 项目配置文件（核心）
├── README.md             # 项目说明
├── .gitignore            # Git 忽略规则
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── models.py     # 数据模型
│       ├── service.py    # 业务逻辑
│       └── utils.py      # 工具函数
├── tests/
│   ├── __init__.py
│   └── test_service.py
└── docs/                 # 文档
```

---

## 2. pyproject.toml

Python 项目的统一配置文件：

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "我的项目"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1",
]

[project.scripts]
my-app = "my_package.__main__:main"
```

---

## 3. uv 常用命令

```powershell
# 初始化项目
uv init my-project
cd my-project

# 添加依赖
uv add requests           # 添加生产依赖
uv add --dev pytest       # 添加开发依赖

# 运行
uv run python main.py     # 在虚拟环境中运行
uv run pytest             # 运行测试

# 管理
uv sync                   # 同步依赖（根据 pyproject.toml）
uv remove requests        # 移除依赖
uv tree                   # 查看依赖树
```

---

## 4. 虚拟环境

虚拟环境让每个项目有独立的依赖，互不干扰：

```powershell
# uv 自动管理虚拟环境（.venv 目录）
# 不需要手动创建和激活

# 如果需要手动激活
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/Mac
```

---

## 5. .gitignore

```
__pycache__/
*.pyc
.venv/
dist/
*.egg-info/
.env
```

---

## 本章小结

- 使用标准目录结构组织项目
- `pyproject.toml` 是项目的核心配置
- `uv` 是现代的包管理工具
- 虚拟环境隔离项目依赖

---

## 下一步

进入 [第 19 章：实战——CLI 待办应用](../19-todo-cli/README.md)。
