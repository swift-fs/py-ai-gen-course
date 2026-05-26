# Pydantic：Python 数据验证利器

> **学习目标**：理解 Pydantic 的核心概念，学会使用 `BaseModel` 定义数据模型、验证输入数据、序列化输出数据，掌握自定义验证器和模型配置。

---

## 1. Pydantic 是什么？

**Pydantic** 是 Python 中最流行的数据验证库。它的核心思想很简单：

> 用 Python 的**类型注解**来定义数据结构，Pydantic 会自动帮你**验证**数据是否符合要求。

### 为什么需要它？

想象你在写一个 Web API，用户提交了一段 JSON 数据：

```json
{"name": "小明", "age": "18", "email": "xm@example.com"}
```

你需要检查：
- `name` 是不是字符串？长度是否合理？
- `age` 是不是整数？（用户传了字符串 `"18"`）
- `email` 格式对不对？

手动写这些检查代码又长又容易出错。Pydantic 帮你一行搞定：

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

user = User(name="小明", age="18", email="xm@example.com")
print(user.age)    # 18（自动把字符串 "18" 转成了整数）
print(type(user.age))  # <class 'int'>
```

### 安装

```powershell
uv add pydantic
# 如果需要 EmailStr 验证，还需要安装 email-validator
uv add "pydantic[email]"
```

---

## 2. BaseModel —— 核心基类

所有 Pydantic 模型都继承自 `BaseModel`。定义模型就像定义一个普通的类：

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int = 0          # 带默认值（可选字段）
    is_active: bool = True
```

### 创建实例的三种方式

```python
# 方式一：关键字参数
user = User(id=1, name="小明", email="xm@example.com", age=18)

# 方式二：字典解包（最常用于 API 开发）
data = {"id": 2, "name": "小红", "email": "xh@example.com"}
user = User(**data)

# 方式三：model_validate（更灵活，推荐）
user = User.model_validate(data)
```

### 访问字段

```python
print(user.name)     # "小红"
print(user.age)      # 0（使用了默认值）
```

---

## 3. 自动类型转换

Pydantic 会尽可能帮你把数据"转换"成目标类型，这在处理外部数据时特别有用：

```python
user = User(id="3", name="小刚", email="xg@example.com", age="20")
print(type(user.id))   # <class 'int'> —— 字符串 "3" 自动转成了整数
print(type(user.age))  # <class 'int'> —— 字符串 "20" 也转了
```

常见转换规则：

| 目标类型 | 可接受的输入 | 示例 |
|---------|------------|------|
| `int` | 数字字符串 | `"18"` → `18` |
| `float` | 整数、数字字符串 | `"3.14"` → `3.14` |
| `str` | 数字、字节 | `b"hello"` → `"hello"` |
| `bool` | 字符串 | `"true"` → `True` |
| `datetime` | ISO 格式字符串 | `"2024-01-01T12:00"` → datetime |

> ⚠️ 转换不是万能的。如果数据确实无法转换（比如把 `"abc"` 转成 `int`），Pydantic 会抛出 `ValidationError`。

---

## 4. 验证错误 ValidationError

当数据不符合要求时，Pydantic 会抛出 `ValidationError`，错误信息非常清晰：

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str

try:
    User(id="not_a_number", name="测试")
except ValidationError as error:
    print(error)
    # 输出类似：
    # 1 validation error for User
    # id
    #   Input should be a valid integer [type=int_parsing, input_value='not_a_number']
```

### 提取错误详情

```python
try:
    User(id="abc", name="测试")
except ValidationError as error:
    for err in error.errors():
        print(f"字段: {err['loc']}")    # 哪个字段出错
        print(f"错误: {err['msg']}")    # 错误描述
        print(f"输入: {err['input']}")  # 用户输入的值
```

---

## 5. Field —— 字段约束

`Field` 可以为字段添加验证规则和元信息：

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="商品名称")
    price: float = Field(gt=0, description="价格必须大于 0")
    stock: int = Field(ge=0, description="库存不能为负数")
    tags: list[str] = Field(default_factory=list, description="标签列表")
```

### 常用的约束参数

| 参数 | 适用类型 | 含义 |
|------|---------|------|
| `gt` / `ge` | 数字 | 大于 / 大于等于 |
| `lt` / `le` | 数字 | 小于 / 小于等于 |
| `min_length` / `max_length` | 字符串、列表 | 最小/最大长度 |
| `pattern` | 字符串 | 正则匹配 |
| `default` | 任意 | 默认值 |
| `default_factory` | 可变类型 | 默认值工厂函数 |
| `description` | 任意 | 字段描述（出现在 JSON Schema 中） |

> 💡 **为什么 `tags` 用 `default_factory=list` 而不是 `default=[]`？**
> 和普通 Python 一样——`default=[]` 会让所有实例共享同一个列表对象，导致数据串改。`default_factory` 每次都会创建新列表。

---

## 6. 自定义验证器

当内置约束不够用时，可以用 `@field_validator` 和 `@model_validator` 编写自定义验证逻辑。

### field_validator —— 验证单个字段

```python
from pydantic import BaseModel, field_validator

class SignupForm(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, value: str) -> str:
        """用户名只能包含字母和数字。"""
        if not value.isalnum():
            raise ValueError("用户名只能包含字母和数字")
        return value
```

### model_validator —— 验证多个字段之间的关系

```python
from pydantic import BaseModel, model_validator

class SignupForm(BaseModel):
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def passwords_match(self) -> "SignupForm":
        """确保两次密码一致。"""
        if self.password != self.password_confirm:
            raise ValueError("两次输入的密码不一致")
        return self
```

### 验证器的执行顺序

1. `mode="before"` 的 `field_validator`（在类型转换之前执行）
2. **类型转换**
3. `mode="after"` 的 `field_validator`（默认值，在类型转换之后执行）
4. `mode="after"` 的 `model_validator`（所有字段验证完毕后执行）

---

## 7. 嵌套模型

模型可以嵌套其他模型，构建复杂的数据结构：

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    district: str
    street: str = ""

class Order(BaseModel):
    order_id: int
    customer_name: str
    items: list[str]
    shipping_address: Address  # 嵌套模型

order = Order(
    order_id=1001,
    customer_name="小明",
    items=["Python 书", "键盘"],
    shipping_address={
        "city": "北京",
        "district": "海淀区",
        "street": "中关村大街1号",
    },
)
print(order.shipping_address.city)  # "北京"
```

> Pydantic 会**递归验证**嵌套模型——`Address` 里的每个字段也会被验证。

---

## 8. 序列化

把模型转回字典或 JSON，用于 API 返回数据、存储等场景。

```python
class User(BaseModel):
    id: int
    name: str
    email: str

user = User(id=1, name="小明", email="xm@example.com")

# 转为字典
user.model_dump()
# {'id': 1, 'name': '小明', 'email': 'xm@example.com'}

# 转为 JSON 字符串
user.model_dump_json()
# '{"id":1,"name":"小明","email":"xm@example.com"}'

# 只包含部分字段
user.model_dump(include={"name", "email"})
# {'name': '小明', 'email': 'xm@example.com'}

# 排除部分字段（比如隐藏密码）
user.model_dump(exclude={"id"})
# {'name': '小明', 'email': 'xm@example.com'}
```

---

## 9. model_validate 和 model_validate_json

从外部数据创建模型的推荐方法：

```python
# 从字典创建（和 User(**data) 类似，但更灵活）
user = User.model_validate({"id": 1, "name": "小明", "email": "xm@example.com"})

# 从 JSON 字符串直接创建（不需要先 json.loads）
json_str = '{"id": 1, "name": "小明", "email": "xm@example.com"}'
user = User.model_validate_json(json_str)
```

---

## 10. computed_field —— 计算字段

根据其他字段自动计算出来的值，序列化时会自动包含：

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

rect = Rectangle(width=5, height=3)
print(rect.area)                      # 15.0
print(rect.model_dump())
# {'width': 5.0, 'height': 3.0, 'area': 15.0}
```

---

## 11. model_config —— 模型配置

通过 `model_config` 控制模型的行为：

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自动去除字符串首尾空格
        extra="forbid",             # 禁止传入未定义的字段
    )

    name: str
    age: int

user = StrictUser(name="  小明  ", age=18)
print(user.name)  # "小明"（空格被自动去掉了）

StrictUser(name="小明", age=18, extra="不允许")  # ❌ 报错：多余字段
```

### 常用配置项

| 配置项 | 默认值 | 含义 |
|-------|--------|------|
| `str_strip_whitespace` | `False` | 自动去除字符串首尾空格 |
| `str_min_length` | `None` | 字符串全局最小长度 |
| `extra` | `"ignore"` | 如何处理多余字段：`"ignore"` 忽略 / `"forbid"` 报错 / `"allow"` 保留 |
| `frozen` | `False` | 为 `True` 时模型不可修改 |
| `populate_by_name` | `False` | 允许通过字段名或别名赋值 |

---

## 12. TypeAdapter —— 验证任意类型

不需要定义 `BaseModel`，也能验证简单类型：

```python
from pydantic import TypeAdapter

# 验证一个列表
adapter = TypeAdapter(list[int])
result = adapter.validate_python(["1", "2", "3"])
print(result)  # [1, 2, 3]

# 验证一个字典
dict_adapter = TypeAdapter(dict[str, float])
result = dict_adapter.validate_python({"pi": "3.14"})
print(result)  # {'pi': 3.14}
```

---

## 13. 模型继承与多场景复用

在实际项目中，同一个实体在不同场景下需要不同的字段（创建、更新、返回），用继承来组织：

```python
from pydantic import BaseModel, EmailStr

class EmployeeBase(BaseModel):
    """基础信息（创建和返回都需要）。"""
    name: str
    department: str

class EmployeeCreate(EmployeeBase):
    """创建时——需要额外字段。"""
    email: EmailStr

class EmployeeUpdate(BaseModel):
    """更新时——所有字段可选。"""
    name: str | None = None
    department: str | None = None

class EmployeePublic(EmployeeBase):
    """返回给前端——包含 id，不含敏感信息。"""
    id: int
```

这种模式在 FastAPI 中非常常见。

---

## 14. 实战案例：博客系统数据模型

综合运用以上知识，设计一个完整的博客文章数据模型：

```python
from datetime import datetime
from pydantic import BaseModel, Field, computed_field, field_validator

class BlogPostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=10)
    tags: list[str] = Field(default_factory=list, max_length=5)

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, tags: list[str]) -> list[str]:
        seen = set()
        result = []
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in seen:
                seen.add(tag)
                result.append(tag)
        return result

class BlogPost(BlogPostCreate):
    id: int
    author: str
    created_at: datetime = Field(default_factory=datetime.now)
    likes: int = 0

    @computed_field
    @property
    def summary(self) -> str:
        return self.content[:50] + "..." if len(self.content) > 50 else self.content
```

---

## 15. 运行配套代码

```powershell
cd 04-tools-and-frameworks/pydantic
uv add pydantic
uv run python pydantic_demo.py
```

配套代码 `pydantic_demo.py` 包含了本章所有示例的可运行版本。

---

## 速查表

| 功能 | 代码 |
|------|------|
| 定义模型 | `class M(BaseModel): ...` |
| 创建实例 | `M(**data)` 或 `M.model_validate(data)` |
| 从 JSON 创建 | `M.model_validate_json(json_str)` |
| 转为字典 | `obj.model_dump()` |
| 转为 JSON | `obj.model_dump_json()` |
| 字段约束 | `Field(gt=0, min_length=1, ...)` |
| 字段验证器 | `@field_validator("name")` |
| 模型验证器 | `@model_validator(mode="after")` |
| 计算字段 | `@computed_field @property` |
| 模型配置 | `model_config = ConfigDict(...)` |
| 验证任意类型 | `TypeAdapter(list[int])` |
