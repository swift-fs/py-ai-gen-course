# 第 18 章：项目结构与 uv

> **学习目标**：掌握 Python 项目的标准目录结构，全面学会使用 uv 管理项目、依赖、虚拟环境和构建发布。

---

## 1. 为什么需要项目结构？

当你写一个简单的脚本（一个 `.py` 文件），直接 `python script.py` 就行。但当项目变大，你会遇到这些问题：

- 多个 `.py` 文件怎么组织？
- 第三方库怎么管理？
- 别人拿到你的代码怎么运行？
- 怎么发布自己的库？

**项目结构**和**包管理器**就是为了解决这些问题的。

---

## 2. uv —— 现代 Python 项目管理工具

`uv` 是用 Rust 编写的超快 Python 工具，替代 pip、virtualenv、poetry 等多个工具：

| 传统工具                        | uv 对应功能                     |
| ------------------------------- | ------------------------------- |
| `pip install`                   | `uv add` / `uv pip install`     |
| `venv`                          | 自动管理（`.venv`）             |
| `pip freeze > requirements.txt` | 自动生成（`uv.lock`）           |
| `poetry`                        | `uv init` / `uv add` / `uv run` |
| `pyenv`                         | `uv python install`             |

### 安装 uv

```powershell
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 验证安装
uv --version
```

---

## 3. 创建项目

### 应用项目（最常用）

```powershell
# 创建新项目
uv init my-app
cd my-app

# 查看生成的文件
```

生成的项目结构：

```
my-app/
├── .python-version     # Python 版本（如 3.12）
├── README.md           # 项目说明
├── main.py             # 入口文件（含示例代码）
└── pyproject.toml      # 项目配置（核心）
```

### 库项目（给别人用的包）

```powershell
uv init --lib my-library
cd my-library
```

```
my-library/
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── my_library/
        ├── __init__.py
        └── py.typed       # 类型标记文件
```

### 在已有目录中初始化

```powershell
mkdir existing-project
cd existing-project
uv init                  # 在当前目录初始化（不会覆盖已有文件）
```

---

## 4. pyproject.toml 详解

`pyproject.toml` 是 Python 项目的**核心配置文件**，所有现代工具都认识它：

```toml
[project]
name = "my-app"                          # 项目名（用于 pip install）
version = "0.1.0"                        # 版本号（语义化版本）
description = "我的第一个项目"            # 简短描述
readme = "README.md"                     # README 文件
requires-python = ">=3.10"               # Python 版本要求
license = "MIT"                          # 开源协议
authors = [                              # 作者信息
    { name = "小明", email = "xm@example.com" }
]

# 生产依赖（运行时需要）
dependencies = [
    "requests>=2.31",                    # HTTP 库
    "rich>=13.0",                        # 终端美化
]

# 可选依赖（分组管理）
[project.optional-dependencies]
dev = [                                  # 开发依赖
    "pytest>=7.0",
    "ruff>=0.1",
]
docs = [                                 # 文档依赖
    "mkdocs>=1.5",
]

# 命令行入口（安装后可直接运行）
[project.scripts]
my-app = "my_app.__main__:main"

# 构建系统
[build-system]
requires = ["hatchling"]                 # 构建工具
build-backend = "hatchling.build"
```

### 版本约束语法

```toml
dependencies = [
    "requests",              # 不限版本（最新）
    "flask>=2.0",            # 大于等于 2.0
    "numpy>=1.24,<2.0",     # 在 1.24 到 2.0 之间
    "pandas==2.1.0",         # 精确版本
    "ruff~=0.1.0",           # 兼容版本（>=0.1.0, <0.2.0）
]
```

### 工具配置

```toml
# ruff 配置
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I"]              # 启用的规则

# pytest 配置
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

## 5. 依赖管理

### 添加依赖

```powershell
# 添加生产依赖
uv add requests                         # 最新版本
uv add "flask>=3.0"                     # 指定版本约束
uv add git+https://github.com/psf/requests  # Git 仓库

# 添加开发依赖（不进生产环境）
uv add --dev pytest
uv add --dev ruff
uv add --dev mypy

# 从 requirements.txt 导入
uv add -r requirements.txt
```

### 移除依赖

```powershell
uv remove requests                      # 移除生产依赖
uv remove --dev pytest                  # 移除开发依赖
```

### 查看依赖

```powershell
uv tree                                 # 查看依赖树（层级结构）
uv pip list                             # 列出已安装的包
```

### 锁文件 uv.lock

每次 `uv add` / `uv remove` 后，uv 会自动更新 `uv.lock` 文件：

```
# uv.lock 的作用：
# 1. 锁定所有依赖的精确版本（包括间接依赖）
# 2. 确保团队成员安装完全相同的版本
# 3. 确保生产环境和开发环境一致
```

> ⚠️ **应该把 `uv.lock` 提交到 Git**，不要加入 `.gitignore`。

---

## 6. 运行和同步

### uv run —— 在项目环境中运行

```powershell
# 运行 Python 脚本（自动同步依赖）
uv run python main.py

# 运行已安装的工具
uv run ruff check .
uv run pytest

# 运行模块
uv run python -m my_app

# 一次性运行（临时安装依赖）
uv run --with httpie httpie get https://api.github.com
```

> `uv run` 会自动确保虚拟环境和依赖是最新的，你不需要手动 `uv sync`。

### uv sync —— 同步环境

```powershell
# 根据 pyproject.toml 和 uv.lock 同步安装
uv sync                                 # 安装生产依赖
uv sync --dev                           # 安装生产 + 开发依赖
uv sync --locked                        # 严格按 lock 文件（CI 用）
uv sync --all-extras                    # 安装所有可选依赖
```

### uv lock —— 仅锁定

```powershell
uv lock                                 # 解析依赖并更新 uv.lock（不安装）
```

---

## 7. 虚拟环境

### uv 的自动管理

uv 会自动在项目目录创建 `.venv` 虚拟环境，**你通常不需要手动操作**：

```powershell
# uv run 自动使用 .venv
uv run python main.py         # 自动在 .venv 中运行

# 如果想手动激活
.venv\Scripts\activate        # Windows PowerShell
source .venv/bin/activate     # Linux/Mac

# 退出虚拟环境
deactivate
```

### 指定 Python 版本

```powershell
# 安装特定 Python 版本
uv python install 3.12

# 查看可用版本
uv python list

# 项目使用特定版本
uv python pin 3.12            # 写入 .python-version 文件
```

---

## 8. 推荐的项目目录结构

### 小型应用（脚本/工具）

```
my-tool/
├── pyproject.toml
├── README.md
├── .python-version
├── .gitignore
├── main.py                   # 入口
├── config.py                 # 配置
└── utils.py                  # 工具函数
```

### 中型项目（多模块应用）

```
my-project/
├── pyproject.toml
├── README.md
├── .python-version
├── .gitignore
├── uv.lock
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── __main__.py       # python -m my_project 的入口
│       ├── models.py
│       ├── service.py
│       └── utils.py
└── tests/
    ├── __init__.py
    └── test_service.py
```

### 库项目（给别人 pip install 的）

```
my-library/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_library/
│       ├── __init__.py
│       ├── core.py
│       └── py.typed
├── tests/
│   └── test_core.py
└── docs/
```

---

## 9. .gitignore 推荐

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# 虚拟环境
.venv/

# 环境变量
.env

# IDE
.vscode/
.idea/

# uv（不要忽略 uv.lock！）
.python-version
```

---

## 10. 完整工作流示例

### 从零开始一个新项目

```powershell
# 1. 创建项目
uv init my-project
cd my-project

# 2. 添加依赖
uv add requests rich
uv add --dev pytest ruff

# 3. 写代码（编辑 main.py 或 src/ 下的文件）

# 4. 运行
uv run python main.py

# 5. 格式化和检查
uv run ruff format .
uv run ruff check --fix .

# 6. 运行测试
uv run pytest

# 7. 提交代码（包括 uv.lock）
git init
git add .
git commit -m "初始项目"
```

### 克隆别人的项目

```powershell
git clone https://github.com/xxx/my-project.git
cd my-project

# 一键安装所有依赖
uv sync

# 运行
uv run python main.py
```

### CI/CD 中的 uv

```powershell
# 严格按 lock 文件安装（确保一致性）
uv sync --locked --all-extras --dev

# 运行测试
uv run pytest
```

---

## 11. uv 命令速查表

| 命令                       | 说明                 |
| -------------------------- | -------------------- |
| `uv init`                  | 创建新项目           |
| `uv add <包名>`            | 添加依赖             |
| `uv add --dev <包名>`      | 添加开发依赖         |
| `uv remove <包名>`         | 移除依赖             |
| `uv run <命令>`            | 在项目环境中运行     |
| `uv sync`                  | 同步安装依赖         |
| `uv sync --locked`         | 严格按 lock 文件安装 |
| `uv lock`                  | 仅更新锁文件         |
| `uv tree`                  | 查看依赖树           |
| `uv pip list`              | 列出已安装的包       |
| `uv python install <版本>` | 安装 Python 版本     |
| `uv python pin <版本>`     | 固定项目 Python 版本 |
| `uv python list`           | 查看可用 Python 版本 |
| `uv build`                 | 构建分发包           |
| `uv publish`               | 发布到 PyPI          |

---

## 本章小结

| 概念             | 说明                               |
| ---------------- | ---------------------------------- |
| `pyproject.toml` | 项目核心配置（元数据、依赖、脚本） |
| `uv init`        | 创建项目                           |
| `uv add/remove`  | 管理依赖                           |
| `uv run`         | 在项目环境中运行命令               |
| `uv sync`        | 同步安装依赖                       |
| `uv.lock`        | 锁文件（确保版本一致）             |
| `.venv`          | 虚拟环境（uv 自动管理）            |
| `src/` 布局      | 推荐的项目目录结构                 |

---

## 下一步

进入 [第 19 章：实战——CLI 待办应用](../19-todo-cli/README.md)。
