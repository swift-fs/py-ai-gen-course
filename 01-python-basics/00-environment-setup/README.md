# 第 0 章：环境搭建

> **学习目标**：安装 Python，学会在终端运行代码，写出你的第一个程序。

---

## 1. Python 是什么？

Python 是一种**编程语言**——人和计算机沟通的语言。你用 Python 写指令，计算机执行指令。

为什么学 Python？
- **语法简单**：读起来像英语，入门容易
- **用途广泛**：网站、数据分析、AI、自动化脚本……
- **社区庞大**：遇到问题容易找到答案

---

## 2. 安装 Python

### Windows

1. 访问 [python.org/downloads](https://www.python.org/downloads/)
2. 下载最新的 Python 3.x（比如 3.12 或 3.13）
3. 运行安装程序
4. ⚠️ **重要**：勾选底部的 **"Add python.exe to PATH"**（将 Python 添加到环境变量）
5. 点击 **Install Now**

### 验证安装

安装完成后，打开**终端**（按 `Win+R`，输入 `cmd`，回车），输入：

```
python --version
```

如果显示类似 `Python 3.12.x`，说明安装成功。

> **什么是终端？** 终端是一个文字界面，你可以输入命令让电脑执行。就像一个"文字版的文件管理器"。

---

## 3. 安装代码编辑器

推荐使用 **VS Code**（Visual Studio Code）——免费、强大、适合初学者。

1. 访问 [code.visualstudio.com](https://code.visualstudio.com/)
2. 下载并安装
3. 安装 **Python 扩展**：打开 VS Code → 左侧点击扩展图标 → 搜索 "Python" → 安装第一个

---

## 4. 运行你的第一个程序

### 方法一：终端直接运行

创建一个文件夹，在里面新建文件 `hello.py`，用 VS Code 打开，输入以下内容：

```python
# 这是你的第一个 Python 程序
# print() 的作用是：把括号里的内容显示在屏幕上
print("Hello, World!")
print("你好，世界！")
print("我正在学习 Python！")
```

然后在终端中运行：

```
python hello.py
```

你会看到：

```
Hello, World!
你好，世界！
我正在学习 Python！
```

### 方法二：VS Code 中运行

1. 打开 `hello.py`
2. 点击右上角的 ▶ 按钮
3. 在下方的终端面板中查看输出

### 方法三：交互式运行

在终端输入 `python` 回车，进入交互模式（`>>>` 提示符）：

```
>>> print("你好")
你好
>>> 1 + 1
2
>>> exit()
```

输入 `exit()` 退出交互模式。

---

## 5. print() 函数详解

`print()` 是你学的第一个函数。它的作用是**在屏幕上显示内容**。

```python
# 显示文字（用引号包裹）
print("你好")

# 显示数字（不需要引号）
print(42)

# 显示计算结果
print(1 + 1)

# 一次显示多个内容（用逗号分隔，自动加空格）
print("我今年", 18, "岁")

# 自定义分隔符
print("2024", "01", "15", sep="-")    # 2024-01-15

# 自定义结尾（默认是换行）
print("第一行", end=" ")
print("第二行")          # 第一行 第二行
```

---

## 6. 什么是注释？

注释是**写给人看的说明**，Python 会忽略它。

```python
# 这是单行注释（以 # 开头）
print("这行会执行")  # 这行后面的注释不会被执行

# 注释的作用：
# 1. 解释代码的含义
# 2. 临时禁用某行代码
# 3. 记录你的想法
```

> 好习惯：写注释解释**为什么**这样做，而不是**做了什么**（代码本身已经说明了做什么）。

---

## 7. uv —— 现代 Python 工具（选读）

`uv` 是一个超快的 Python 包管理工具。后续进阶教程会用到它，现在只需了解：

```powershell
# 安装 uv（Windows PowerShell）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 创建项目
uv init my-project
cd my-project

# 运行代码
uv run python hello.py
```

> 现在阶段不需要安装 uv，等后面需要管理第三方库时再学。

---

## 本章小结

| 概念 | 说明 |
|------|------|
| Python | 编程语言，语法简单，用途广泛 |
| 终端 | 文字界面，输入命令执行操作 |
| `python hello.py` | 在终端运行 Python 文件 |
| `print()` | 在屏幕上显示内容 |
| 注释 `#` | 写给人看的说明，Python 忽略 |
| VS Code | 代码编辑器，写代码的工具 |

---

## 下一步

进入 [第 1 章：变量与数据类型](../01-variables-and-types/README.md)。
