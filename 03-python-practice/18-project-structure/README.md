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

uv 支持**三种项目模式**，适用于不同场景：

| 模式     | 命令                       | 适用场景                       |
| -------- | -------------------------- | ------------------------------ |
| 普通应用 | `uv init my-app`           | 脚本、工具、简单项目           |
| 打包应用 | `uv init --package my-app` | 需要定义命令行入口、测试、发布 |
| 库项目   | `uv init --lib my-lib`     | 给别人 `pip install` 用的包    |

### 普通应用项目

最简单的模式，适合脚本和小工具：

```powershell
uv init my-app
cd my-app
```

生成的项目结构：

```
my-app/
├── .python-version     # Python 版本（如 3.12）
├── README.md           # 项目说明
├── main.py             # 入口文件（含示例代码）
└── pyproject.toml      # 项目配置（核心）
```

对应的 `pyproject.toml`（注意没有 `[build-system]`）：

```toml
[project]
name = "my-app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

> **关键区别**：普通应用**没有构建系统**，不会被"安装"到虚拟环境中，代码直接从项目目录运行。

### 打包应用项目（`--package`）

当你需要**定义命令行入口**、**编写测试**或**发布到 PyPI** 时，使用 `--package`：

```powershell
uv init --package my-cli-tool
cd my-cli-tool
```

生成的项目结构：

```
my-cli-tool/
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── my_cli_tool/
        └── __init__.py   # 含 main() 示例函数
```

对应的 `pyproject.toml`（有 `[build-system]` 和 `[project.scripts]`）：

```toml
[project]
name = "my-cli-tool"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
my-cli-tool = "my_cli_tool:main"    # 命令行入口

[build-system]
requires = ["uv_build>=0.11.16,<0.12"]
build-backend = "uv_build"
```

> **打包应用会被安装到 `.venv` 中**，所以 `uv run my-cli-tool` 可以直接调用入口命令。

### 库项目（`--lib`）

给别人 `pip install` 用的包：

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
        ├── __init__.py     # 库的入口
        └── py.typed        # 类型标记文件（告诉类型检查器这个包有类型提示）
```

对应的 `pyproject.toml`：

```toml
[project]
name = "my-library"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["uv_build>=0.11.16,<0.12"]
build-backend = "uv_build"
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
my-app = "my_app:main"

# 构建系统（uv 自带的构建后端，比 hatchling 快 10-30 倍）
[build-system]
requires = ["uv_build>=0.11.16,<0.12"]
build-backend = "uv_build"
```

> **关于构建后端**：uv 现在有了自己的 `uv_build` 构建后端，比传统的 `hatchling` 快 10-30 倍。`uv init --lib` 和 `uv init --package` 会自动使用它。普通应用（不带 `--package`）不需要构建系统。

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

`uv run` 是在项目环境中运行命令的**唯一推荐方式**。它会自动确保 `.venv` 虚拟环境和依赖是最新的。

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

# 运行项目定义的命令行入口
uv run my-cli-tool
```

> `uv run` 会自动确保虚拟环境和依赖是最新的，你不需要手动 `uv sync`。

### uv run 的模块发现机制

`uv run` 的工作方式取决于项目类型：

#### 普通应用（无 `[build-system]`）

```
my-app/
├── pyproject.toml       # 无 build-system
├── main.py
└── utils.py
```

uv 会把**项目根目录**加入 `sys.path`，所以你可以直接 `import` 同目录的模块：

```powershell
# main.py 中有 import utils，直接能找到
uv run python main.py

# 也可以直接 import 项目根目录下的任何 .py 文件
uv run python -c "import utils; utils.hello()"
```

#### 打包应用 / 库项目（有 `[build-system]`）

```
my-cli-tool/
├── pyproject.toml       # 有 build-system + uv_build
└── src/
    └── my_cli_tool/
        ├── __init__.py
        └── service.py
```

uv 会把项目**构建并安装到 `.venv` 中**（可编辑模式），Python 从 `src/my_cli_tool/` 查找模块：

```powershell
# Python 知道去哪里找 my_cli_tool 包
uv run python -c "from my_cli_tool.service import hello; hello()"

# 通过 -m 运行包（需要包目录下有 __main__.py）
uv run python -m my_cli_tool

# 通过 project.scripts 定义的入口运行
uv run my-cli-tool
```

#### 模块名规范化规则

uv 会自动规范化包名：

| `pyproject.toml` 中的 name | 模块目录名 | 说明                     |
| -------------------------- | ---------- | ------------------------ |
| `my-app`                   | `my_app`   | 连字符 → 下划线          |
| `My.App`                   | `my_app`   | 大写 → 小写，点 → 下划线 |
| `cool_lib`                 | `cool_lib` | 不变                     |

默认在 `src/` 目录下查找模块，即 `src/<规范化名称>/__init__.py`。

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

## 8. 命令行入口详解（project.scripts）

当你的项目是一个 CLI 工具或需要提供命令行命令时，使用 `[project.scripts]` 定义入口点：

### 基本语法

```toml
[project.scripts]
命令名 = "模块路径:函数名"
```

格式为 `包名.模块:函数`，其中函数必须是**无参数的可调用对象**（或者接受 `sys.argv` 参数的函数）。

### 示例

假设项目结构如下：

```
my-cli-tool/
├── pyproject.toml
└── src/
    └── my_cli_tool/
        ├── __init__.py      # 包入口
        ├── cli.py           # CLI 逻辑
        └── core.py          # 核心功能
```

**在 `src/my_cli_tool/__init__.py` 中定义入口函数**：

```python
def main():
    """CLI 入口函数"""
    print("Hello from my-cli-tool!")

if __name__ == "__main__":
    main()
```

**在 `pyproject.toml` 中声明入口**：

```toml
[project.scripts]
my-cli-tool = "my_cli_tool:main"
```

**也可以指向子模块中的函数**：

```toml
[project.scripts]
my-cli-tool = "my_cli_tool.cli:main"
my-cli-tool-greet = "my_cli_tool.cli:greet_command"
```

> ⚠️ 使用 `[project.scripts]` 需要项目是**打包模式**（`uv init --package` 或 `uv init --lib`），普通应用不支持。

### 运行入口命令

```powershell
# 通过 uv run 运行（推荐）
uv run my-cli-tool

# 等价于
uv run python -c "from my_cli_tool import main; main()"
```

### GUI 应用入口

如果是 GUI 应用（如 tkinter、PyQt），使用 `[project.gui-scripts]`：

```toml
[project.gui-scripts]
my-gui-app = "my_gui:run_app"
```

区别在于 `gui-scripts` 在 Windows 上不会弹出命令行窗口。

---

## 9. 构建与发布

### 构建分发包

当你想把项目打包成 `.whl` 和 `.tar.gz` 文件：

```powershell
# 构建当前项目
uv build

# 查看生成的文件
# dist/
# ├── my_library-0.1.0-py3-none-any.whl   # wheel 包
# └── my_library-0.1.0.tar.gz             # 源码包
```

### 发布到 PyPI

```powershell
# 发布到 PyPI（需要账号）
uv publish

# 发布到测试 PyPI
uv publish --publish-url https://test.pypi.org/legacy/

# 使用 token 认证
uv publish --token pypi-xxx
```

### 本地安装测试

```powershell
# 在另一个项目中安装本地包进行测试
uv add --dev ../my-library

# 或者用构建好的 wheel 安装
uv add --dev ./dist/my_library-0.1.0-py3-none-any.whl
```

---

## 10. 自定义模块路径

默认情况下，`uv_build` 在 `src/` 目录下查找与项目名对应的模块。如果你的项目结构不同，可以自定义：

### 非 src 布局（扁平布局）

```
my-project/
├── pyproject.toml
└── my_project/          # 模块直接在根目录下（不在 src/ 中）
    └── __init__.py
```

```toml
[tool.uv.build-backend]
module-root = ""          # 告诉 uv_build 在项目根目录查找模块
```

### 自定义模块名

如果模块目录名和项目名不匹配：

```
my-project/
├── pyproject.toml
└── src/
    └── custom_name/      # 模块名和项目名不一致
        └── __init__.py
```

```toml
[tool.uv.build-backend]
module-name = "custom_name"    # 指定实际的模块名
```

### 纯虚拟项目（不打包）

如果一个项目只用来管理依赖，不需要被安装：

```toml
[tool.uv]
package = false            # 项目本身不会被安装到 .venv

[build-system]
requires = ["uv_build>=0.11.16,<0.12"]
build-backend = "uv_build"
```

---

## 11. 内联脚本依赖（PEP 723）

如果你只是写一个**单文件脚本**，不想创建完整项目，可以使用内联依赖声明：

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.31",
#     "rich>=13.0",
# ]
# ///

import requests
from rich import print

response = requests.get("https://api.github.com")
print(f"Status: {response.status_code}")
```

运行方式：

```powershell
# 直接运行（自动安装依赖）
uv run script.py

# 也可以给脚本添加依赖
uv add --script script.py beautifulsoup4
```

> `uv run script.py` 会自动读取脚本中的 `# /// script` 块，创建临时环境并安装依赖。不需要 `pyproject.toml`。

---

## 12. 推荐的项目目录结构

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

> 使用 `uv init --package` 创建，需要 `[build-system]` 和 `[project.scripts]`。

```
my-project/
├── pyproject.toml
├── README.md
├── .python-version
├── .gitignore
├── uv.lock
├── src/
│   └── my_project/
│       ├── __init__.py       # 包入口（定义 main()）
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

## 13. .gitignore 推荐

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

## 14. 完整工作流示例

### 从零开始一个普通应用

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

### 创建一个 CLI 工具（打包应用）

```powershell
# 1. 创建打包应用
uv init --package my-cli-tool
cd my-cli-tool

# 2. 添加依赖（如 click 用于命令行参数解析）
uv add click

# 3. 编辑 src/my_cli_tool/__init__.py，实现 main() 函数

# 4. 运行入口命令
uv run my-cli-tool

# 5. 也可以用 python -m 运行
uv run python -m my_cli_tool

# 6. 测试
uv add --dev pytest
uv run pytest

# 7. 构建并发布
uv build
uv publish
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

## 15. uv 命令速查表

| 命令                         | 说明                      |
| ---------------------------- | ------------------------- |
| `uv init`                    | 创建普通应用项目          |
| `uv init --package`          | 创建打包应用项目          |
| `uv init --lib`              | 创建库项目                |
| `uv add <包名>`              | 添加依赖                  |
| `uv add --dev <包名>`        | 添加开发依赖              |
| `uv add --script 文件.py 包` | 给单文件脚本添加依赖      |
| `uv remove <包名>`           | 移除依赖                  |
| `uv run <命令>`              | 在项目环境中运行          |
| `uv run <入口名>`            | 运行 project.scripts 入口 |
| `uv sync`                    | 同步安装依赖              |
| `uv sync --locked`           | 严格按 lock 文件安装      |
| `uv lock`                    | 仅更新锁文件              |
| `uv tree`                    | 查看依赖树                |
| `uv pip list`                | 列出已安装的包            |
| `uv python install <版本>`   | 安装 Python 版本          |
| `uv python pin <版本>`       | 固定项目 Python 版本      |
| `uv python list`             | 查看可用 Python 版本      |
| `uv build`                   | 构建分发包                |
| `uv publish`                 | 发布到 PyPI               |

---

## 本章小结

| 概念                | 说明                                          |
| ------------------- | --------------------------------------------- |
| `pyproject.toml`    | 项目核心配置（元数据、依赖、脚本）            |
| `uv init`           | 创建普通应用                                  |
| `uv init --package` | 创建打包应用（有构建系统、可定义入口）        |
| `uv init --lib`     | 创建库项目                                    |
| `uv_build`          | uv 自带的构建后端（比 hatchling 快 10-30 倍） |
| `[project.scripts]` | 定义命令行入口（打包应用/库项目可用）         |
| `uv run`            | 在项目环境中运行命令（自动同步依赖）          |
| `uv run 入口名`     | 运行 project.scripts 定义的命令               |
| `uv add/remove`     | 管理依赖                                      |
| `uv sync`           | 同步安装依赖                                  |
| `uv.lock`           | 锁文件（确保版本一致）                        |
| `.venv`             | 虚拟环境（uv 自动管理）                       |
| `src/` 布局         | 推荐的项目目录结构                            |
| `uv build`          | 构建分发包（.whl + .tar.gz）                  |
| `uv publish`        | 发布到 PyPI                                   |
| PEP 723 内联脚本    | 单文件脚本的依赖声明方式                      |

---

## 下一步

进入 [第 19 章：实战——CLI 待办应用](../19-todo-cli/README.md)。
