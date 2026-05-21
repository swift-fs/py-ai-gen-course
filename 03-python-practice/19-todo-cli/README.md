# 第 19 章：实战——CLI 待办应用

> **学习目标**：综合运用前面所学，构建一个完整的命令行待办事项应用。

---

## 项目概述

我们要构建一个 CLI 待办应用，具备以下功能：
- 添加、删除、完成任务
- 列出所有任务
- 数据持久化到 JSON 文件

### 项目结构

```
todo-app/
├── pyproject.toml
├── todo_app/
│   ├── __init__.py
│   ├── __main__.py      # 入口
│   ├── models.py        # 数据模型
│   ├── storage.py       # 存储层
│   └── service.py       # 业务逻辑
└── todos.json            # 数据文件（运行后生成）
```

---

## 代码实现

### models.py —— 数据模型

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Todo:
    title: str
    done: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    def toggle(self):
        self.done = not self.done

    def __str__(self):
        status = "✓" if self.done else "○"
        return f"  [{status}] {self.title} ({self.created_at})"
```

### storage.py —— 存储层

```python
import json
from pathlib import Path
from .models import Todo

class TodoStorage:
    def __init__(self, file_path="todos.json"):
        self.path = Path(file_path)

    def load(self) -> list[Todo]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Todo(**item) for item in data]

    def save(self, todos: list[Todo]):
        data = [{"title": t.title, "done": t.done, "created_at": t.created_at} for t in todos]
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
```

### service.py —— 业务逻辑

```python
from .models import Todo
from .storage import TodoStorage

class TodoService:
    def __init__(self, storage: TodoStorage):
        self.storage = storage
        self.todos = storage.load()

    def add(self, title: str):
        self.todos.append(Todo(title=title))
        self._save()

    def remove(self, index: int):
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self._save()
            return True
        return False

    def toggle(self, index: int):
        if 0 <= index < len(self.todos):
            self.todos[index].toggle()
            self._save()
            return True
        return False

    def list_all(self):
        return self.todos

    def _save(self):
        self.storage.save(self.todos)
```

### __main__.py —— CLI 入口

```python
import sys
from .storage import TodoStorage
from .service import TodoService

def main():
    service = TodoService(TodoStorage())
    args = sys.argv[1:]

    if not args:
        print("用法: python -m todo_app [命令]")
        print("  add <内容>    添加任务")
        print("  list          列出任务")
        print("  done <编号>   完成/取消完成任务")
        print("  remove <编号> 删除任务")
        return

    command = args[0]

    if command == "add" and len(args) > 1:
        service.add(" ".join(args[1:]))
        print("已添加")
    elif command == "list":
        todos = service.list_all()
        if not todos:
            print("暂无任务")
        for i, todo in enumerate(todos):
            print(f"  {i}. {todo}")
    elif command == "done" and len(args) > 1:
        if service.toggle(int(args[1])):
            print("已更新")
        else:
            print("编号无效")
    elif command == "remove" and len(args) > 1:
        if service.remove(int(args[1])):
            print("已删除")
        else:
            print("编号无效")
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
```

---

## 运行方式

```powershell
cd todo-app
python -m todo_app add 学习 Python
python -m todo_app add 写项目
python -m todo_app list
python -m todo_app done 0
python -m todo_app remove 1
```

---

## 本章小结

- 分层架构：models（数据）→ storage（存储）→ service（逻辑）→ CLI（界面）
- 使用 dataclass 定义数据模型
- JSON 文件持久化
- `sys.argv` 处理命令行参数

---

## 下一步

进入 [第 20 章：实战——Web API](../20-web-api/README.md)。
