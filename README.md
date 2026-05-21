# Python AI 课程

从零基础到实战的 Python 完整学习路径。

## 课程结构

```
python-ai-course/
│
├── 01-python-basics/              # 入门篇：Python 基础
│   ├── 00-environment-setup/      #   环境搭建（Python + uv + VS Code）
│   ├── 01-syntax-basics/          #   语法基础（变量、类型、运算符、字符串）
│   ├── 02-data-structures/        #   数据结构（列表、元组、字典、集合、推导式）
│   ├── 03-control-flow/           #   控制流（条件、循环、模式匹配）
│   ├── 04-functions/              #   函数（参数、高阶函数、闭包、递归）
│   ├── 05-modules-and-packages/   #   模块与包（标准库、导入规范）
│   └── 06-file-io/                #   文件 I/O（文本、二进制、CSV、JSON）
│
├── 02-python-advanced/            # 进阶篇：深入 Python
│   ├── 00-oop/                    #   面向对象（类、继承、多态、dataclass）
│   ├── 01-decorators/             #   装饰器（函数装饰器、类装饰器、实用模式）
│   ├── 02-generators/             #   生成器（yield、惰性求值、数据管道）
│   ├── 03-async/                  #   异步编程（async/await、asyncio、并发模式）
│   ├── 04-type-annotations/       #   类型注解（泛型、Protocol、高级类型）
│   ├── 05-design-patterns/        #   设计模式（创建型、结构型、行为型）
│   ├── 06-error-handling/         #   错误处理（异常、自定义异常、日志）
│   └── 07-testing/                #   测试（pytest、参数化、夹具）
│
├── 03-python-practice/            # 实战篇：项目实战
│   ├── 00-project-structure/      #   项目结构（pyproject.toml、src 布局）
│   ├── 01-uv-deep-dive/           #   uv 深度使用（版本管理、工具安装、CI/CD）
│   ├── 02-todo-cli-app/           #   实战：CLI 待办应用
│   └── 03-web-api/                #   实战：FastAPI Web API
│
└── 04-tools-and-frameworks/       # 工具与框架汇总
    ├── package-managers.md        #   包管理器（uv, pip, poetry）
    ├── web-frameworks.md          #   Web 框架（FastAPI, Django, Flask）
    ├── database-tools.md          #   数据库（SQLAlchemy, SQLModel）
    ├── data-science.md            #   数据科学（pandas, numpy, matplotlib）
    ├── testing-tools.md           #   测试工具（pytest, unittest）
    ├── code-quality.md            #   代码质量（ruff, mypy, pre-commit）
    ├── async-tools.md             #   异步工具（httpx, aiofiles）
    ├── cli-tools.md               #   CLI 工具（click, typer, rich）
    └── task-queues.md             #   任务队列（celery, arq, huey）
```

## 学习路线

### 阶段一：入门（第 0-6 章）

适合零基础学习者，从环境搭建开始，逐步掌握 Python 基本语法。

```powershell
# 每章都可以直接运行示例代码
cd 01-python-basics/01-syntax-basics
uv run python variables_and_types.py
```

### 阶段二：进阶（第 7-14 章）

深入理解 Python 的高级特性，写出更优雅、更专业的代码。

```powershell
cd 02-python-advanced/04-type-annotations
uv run python type_basics.py
```

### 阶段三：实战（第 15-18 章）

综合运用所学知识，构建完整的项目。

```powershell
# CLI 待办应用
cd 03-python-practice/02-todo-cli-app
uv run python -m todo_app add "学习 Python"
uv run python -m todo_app list

# Web API
cd 03-python-practice/03-web-api
uv add fastapi uvicorn
uv run python -m uvicorn app.main:app --reload
```

## 环境要求

- **Python**: 3.11+
- **包管理器**: uv（推荐）或 pip
- **编辑器**: VS Code（推荐安装 Python、Pylance、Ruff 扩展）

## 快速开始

```powershell
# 安装 uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 克隆项目后，任意章节的代码都可以直接运行
uv run python 文件名.py
```

## 课程特色

- **代码可直接运行**：每个示例都经过验证，复制即可运行
- **类型注解**：所有代码使用现代 Python 类型注解
- **最新实践**：通过 Context7 获取最新文档，确保用法不过时
- **循序渐进**：从基础到进阶到实战，平滑过渡
- **工具汇总**：常用框架和工具的快速参考
