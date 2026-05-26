# FastAPI：现代 Python Web 框架

> **学习目标**：理解 FastAPI 的核心概念，学会创建 REST API、处理请求参数、使用 Pydantic 模型验证数据、使用依赖注入组织代码，完成一个完整的 CRUD 项目。

---

## 1. FastAPI 是什么？

**FastAPI** 是一个现代、高性能的 Python Web 框架，用来构建 API（后端接口）。它的核心特点：

| 特点         | 说明                                  |
| ------------ | ------------------------------------- |
| **快**       | 性能媲美 Node.js 和 Go                |
| **简单**     | 用 Python 类型注解就能定义 API        |
| **自动文档** | 自动生成交互式 API 文档（Swagger UI） |
| **数据验证** | 内置 Pydantic，自动验证请求和响应     |
| **异步支持** | 原生支持 `async/await`                |

### 安装

```powershell
uv add fastapi uvicorn
```

- `fastapi`：框架本身
- `uvicorn`：ASGI 服务器，用来运行 FastAPI 应用

---

## 2. 第一个 FastAPI 应用

创建一个文件 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

逐行解读：
- `app = FastAPI()` —— 创建一个 FastAPI 应用实例，这是整个应用的核心对象
- `@app.get("/")` —— **装饰器**，告诉 FastAPI："当有人用 GET 方法访问 `/` 路径时，执行下面的函数"
- `async def root()` —— 路由处理函数，返回的字典会被 FastAPI 自动转成 JSON

### 运行

```powershell
uv run python -m uvicorn main:app --reload
```

- `main`：文件名（`main.py`）
- `app`：FastAPI 实例的变量名
- `--reload`：代码修改后自动重启（开发时使用）

打开浏览器访问：
- **http://127.0.0.1:8000** —— API 返回结果
- **http://127.0.0.1:8000/docs** —— 自动生成的交互式文档 🎉
- **http://127.0.0.1:8000/redoc** —— 另一种风格的文档

> 💡 `/docs` 页面可以直接测试 API，不需要 Postman！

---

## 3. 路由与 HTTP 方法

**路由**决定了"哪个 URL 对应哪个函数"。**HTTP 方法**表示操作类型：

| 方法     | 用途     | 示例             |
| -------- | -------- | ---------------- |
| `GET`    | 获取数据 | 获取商品列表     |
| `POST`   | 创建数据 | 新建一个商品     |
| `PUT`    | 完整更新 | 替换整个商品信息 |
| `PATCH`  | 部分更新 | 只修改商品价格   |
| `DELETE` | 删除数据 | 删除一个商品     |

```python
from fastapi import FastAPI

app = FastAPI()

items = []

@app.get("/items")
async def list_items():
    return items

@app.post("/items", status_code=201)
async def create_item(name: str):
    items.append({"name": name})
    return {"message": f"已创建: {name}"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"已删除: {item_id}"}
```

> `status_code=201` 表示"已创建"。FastAPI 默认返回 200（成功），创建资源通常用 201。

---

## 4. 路径参数 Path Parameters

URL 中用 `{}` 包裹的部分就是路径参数：

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}
```

访问 `/items/42`，`item_id` 的值就是 `42`。

### 类型自动转换和验证

FastAPI 会自动把路径参数转成声明的类型：

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):  # 声明为 int
    ...
```

- 访问 `/items/42` → `item_id = 42`（整数）
- 访问 `/items/abc` → 自动返回 422 错误（`abc` 不是整数）

### 路径顺序很重要

```python
# ✅ 正确：具体路径在前
@app.get("/items/me")
async def get_my_items(): ...

@app.get("/items/{item_id}")
async def get_item(item_id: int): ...

# ❌ 错误：如果 {item_id} 在前，访问 /items/me 时 item_id 会等于 "me"
```

---

## 5. 查询参数 Query Parameters

### 5.1 什么是查询参数？

URL 中 `?` 后面的键值对就是查询参数，多个参数用 `&` 分隔：

```
/items?keyword=Python&min_price=10
```

上面这个 URL 中有两个查询参数：
- `keyword` = `"Python"`
- `min_price` = `10`

### 5.2 最简单的查询参数——直接用类型注解

在函数参数中声明查询参数，最简单的方式就是直接给默认值：

```python
@app.get("/items")
async def search_items(keyword: str = "", limit: int = 10):
    return {"keyword": keyword, "limit": limit}
```

访问 `/items?keyword=Python&limit=5` 时：
- `keyword` = `"Python"`
- `limit` = `5`

访问 `/items`（不带参数）时：
- `keyword` = `""` （使用默认值）
- `limit` = `10`（使用默认值）

> **规则**：有默认值的参数是**可选的**，没有默认值的参数是**必填的**。

### 5.3 用 Query() 添加验证和文档

直接用类型注解虽然简单，但你无法限制参数的范围、长度等。比如用户传 `limit=99999`，你无法阻止。这时就需要 `Query()`。

`Query()` 是 FastAPI 提供的一个函数，用来给查询参数添加：
- **默认值**（第一个参数）
- **数值范围验证**：`gt`（大于）、`ge`（大于等于）、`lt`（小于）、`le`（小于等于）
- **字符串长度验证**：`min_length`、`max_length`
- **API 文档描述**：`title`、`description`
- **别名**：`alias`（当 URL 参数名不是合法 Python 变量名时使用）
- **标记废弃**：`deprecated=True`

```python
from fastapi import Query

@app.get("/items")
async def search_items(
    keyword: str = Query(default="", description="搜索关键词"),
    min_price: float = Query(default=0, ge=0, description="最低价格，不能为负数"),
    max_price: float = Query(default=None, ge=0, description="最高价格，不能为负数"),
    limit: int = Query(default=10, ge=1, le=100, description="返回数量，1~100之间"),
):
    return {"keyword": keyword, "min_price": min_price, "limit": limit}
```

逐个解读：
- `Query(default="", description="搜索关键词")` —— 默认值是空字符串，API 文档中会显示"搜索关键词"这个描述
- `Query(default=0, ge=0)` —— `ge=0` 表示 **g**reater than or **e**qual to 0，即 `>= 0`，用户传 `-1` 会被拒绝
- `Query(default=10, ge=1, le=100)` —— 限制 `limit` 在 1~100 之间，`le` 是 **l**ess than or **e**qual

如果用户传了不符合条件的值，FastAPI 会自动返回 422 错误：

```json
{
    "detail": [
        {
            "type": "greater_than_equal",
            "loc": ["query", "limit"],
            "msg": "Input should be greater than or equal to 1",
            "input": "0"
        }
    ]
}
```

### 5.4 Query() 所有验证参数速查

| 参数          | 类型  | 说明                   | 示例                          |
| ------------- | ----- | ---------------------- | ----------------------------- |
| `default`     | 任意  | 默认值，`...` 表示必填 | `Query(default=10)`           |
| `gt`          | float | 大于                   | `Query(gt=0)` → 必须 > 0      |
| `ge`          | float | 大于等于               | `Query(ge=0)` → 必须 >= 0     |
| `lt`          | float | 小于                   | `Query(lt=100)` → 必须 < 100  |
| `le`          | float | 小于等于               | `Query(le=100)` → 必须 <= 100 |
| `min_length`  | int   | 字符串最小长度         | `Query(min_length=1)`         |
| `max_length`  | int   | 字符串最大长度         | `Query(max_length=50)`        |
| `description` | str   | API 文档中的描述       | `Query(description="页码")`   |
| `alias`       | str   | URL 中的参数别名       | `Query(alias="item-query")`   |
| `deprecated`  | bool  | 标记为已废弃           | `Query(deprecated=True)`      |

### 5.5 alias 别名的使用场景

有时 URL 参数名包含连字符（如 `item-query`），但这不是合法的 Python 变量名。这时用 `alias`：

```python
@app.get("/items")
async def read_items(item_query: str = Query(alias="item-query")):
    return {"item_query": item_query}
```

访问 `/items?item-query=Python`，FastAPI 会用别名 `item-query` 从 URL 中取值，赋给 Python 变量 `item_query`。

### 5.6 参数类型总结

| 类型            | 说明                | 示例                            |
| --------------- | ------------------- | ------------------------------- |
| 有默认值        | 可选参数            | `limit: int = 10`               |
| `Optional[str]` | 可选，可能为 `None` | `keyword: Optional[str] = None` |
| `Query(...)`    | 带验证的查询参数    | `Query(ge=1, le=100)`           |
| 无默认值        | **必填**            | `keyword: str`                  |

---

## 6. 请求体 Request Body

`POST`、`PUT`、`PATCH` 通常需要客户端发送数据（JSON 格式）。用 **Pydantic 模型**来定义请求体。

### 6.1 Pydantic 是什么？

Pydantic 是一个数据验证库。你用 Python 类定义数据的"形状"（有哪些字段、什么类型），Pydantic 会自动：
- 把 JSON 转成 Python 对象
- 验证数据类型和约束
- 验证失败时返回清晰的错误信息

### 6.2 定义请求体模型

```python
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, description="商品名称")
    price: float = Field(gt=0, description="价格")
    tags: list[str] = Field(default_factory=list)
```

逐行解读：
- `BaseModel` —— Pydantic 的基类，所有请求体模型都要继承它
- `name: str = Field(min_length=1)` —— `name` 是字符串，至少 1 个字符。`Field()` 的作用和 `Query()` 类似，都是给字段添加验证规则
- `price: float = Field(gt=0)` —— 价格必须是浮点数，且大于 0
- `tags: list[str] = Field(default_factory=list)` —— `default_factory=list` 表示如果不传 `tags`，默认是空列表。注意不能用 `tags: list[str] = []`，因为 Python 中可变默认值会导致所有实例共享同一个列表

### 6.3 Field() 常用验证参数

| 参数              | 说明             | 示例                            |
| ----------------- | ---------------- | ------------------------------- |
| `min_length`      | 字符串最小长度   | `Field(min_length=1)`           |
| `max_length`      | 字符串最大长度   | `Field(max_length=100)`         |
| `gt`              | 大于             | `Field(gt=0)` → 必须 > 0        |
| `ge`              | 大于等于         | `Field(ge=0)` → 必须 >= 0       |
| `lt`              | 小于             | `Field(lt=10000)`               |
| `le`              | 小于等于         | `Field(le=10000)`               |
| `default`         | 默认值           | `Field(default=0)`              |
| `default_factory` | 默认值工厂函数   | `Field(default_factory=list)`   |
| `description`     | API 文档中的描述 | `Field(description="商品名称")` |

### 6.4 在路由中使用请求体

```python
@app.post("/items", status_code=201)
async def create_item(item: ItemCreate):
    # FastAPI 自动完成三件事：
    # 1. 读取请求体中的 JSON
    # 2. 用 ItemCreate 模型验证数据
    # 3. 创建 ItemCreate 实例赋给 item 参数
    print(item.name)   # "Python 书"
    print(item.price)  # 59.9
    print(item.tags)   # ["编程"]
    return {"message": "创建成功"}
```

客户端发送的 JSON：
```json
{"name": "Python 书", "price": 59.9, "tags": ["编程"]}
```

> **FastAPI 怎么知道 `item` 是请求体？** 因为它的类型是 `ItemCreate`（Pydantic 模型），不是 `int`、`str` 这些基本类型，FastAPI 就会把它当作请求体来解析。

### 6.5 自定义验证器

除了 `Field` 的内置验证，你还可以用 `@field_validator` 写自定义验证逻辑：

```python
from pydantic import field_validator

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        # 去掉首尾空格后检查是否为空
        value = value.strip()
        if not value:
            raise ValueError("商品名称不能全是空格")
        return value
```

当用户发送 `{"name": "   ", "price": 10}` 时，验证器会拒绝并返回错误。

---

## 7. 响应模型 Response Model

### 7.1 为什么需要响应模型？

如果没有 `response_model`，你的函数返回什么，客户端就收到什么。但很多时候你希望：
- **隐藏敏感字段**（如密码、内部 ID）
- **确保输出格式一致**（即使内部数据结构不同）
- **让 API 文档显示返回格式**

### 7.2 定义和使用

```python
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    tags: list[str]

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    # 即使返回的是字典，FastAPI 也会按 ItemResponse 的格式过滤和转换
    return {"id": item_id, "name": "Python 书", "price": 59.9, "tags": ["编程"], "internal_note": "仅供内部使用"}
```

上面的 `internal_note` 字段不会出现在客户端收到的响应中，因为 `ItemResponse` 没有这个字段。

### 7.3 不同场景用不同模型

实际项目中，创建、更新、返回通常用不同的模型：

```python
class ItemCreate(BaseModel):
    """创建时用——客户端需要提供的数据。"""
    name: str
    price: float

class ItemUpdate(BaseModel):
    """更新时用——所有字段可选。"""
    name: str | None = None
    price: float | None = None

class ItemResponse(BaseModel):
    """返回时用——包含服务端生成的 id。"""
    id: int
    name: str
    price: float

@app.post("/items", response_model=ItemResponse)
async def create(item: ItemCreate):
    # ItemCreate 里没有 id，ItemResponse 里有
    # 这样客户端不需要传 id，但能收到带 id 的响应
    new_item = {"id": 1, **item.model_dump()}
    return new_item
```

### 7.4 response_model 的三大好处

1. **过滤输出字段**：内部数据有 `password`，但响应模型没有，自动隐藏
2. **类型转换**：确保输出数据的类型正确（如把 `Decimal` 转成 `float`）
3. **文档生成**：自动文档会显示响应的数据结构

---

## 8. 依赖注入 Dependency Injection

> 这是本教程最重要的概念之一，请仔细阅读。

### 8.1 什么是"依赖"？

假设你在写一个外卖系统，有以下路由：

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # 查找商品，找不到就报 404
    item = find_item_or_404(item_id)
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, data: ItemUpdate):
    # 又要查找商品，找不到就报 404
    item = find_item_or_404(item_id)
    item.update(data.model_dump())
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    # 还是要查找商品...
    item = find_item_or_404(item_id)
    db.remove(item)
    return {"message": "已删除"}
```

每个路由都要先"查找商品，找不到就 404"——这段逻辑被重复了三次。如果以后查找逻辑要改（比如加了缓存），你得改三个地方。

**"查找商品"就是一个"依赖"**——多个路由都依赖于这个操作。

### 8.2 依赖注入解决什么问题？

**依赖注入（Dependency Injection，简称 DI）** 的核心思想：

> 把公共逻辑提取成一个函数/类，FastAPI 会在调用路由函数之前自动执行它，把结果传给你的路由函数。

用依赖注入改写上面的代码：

```python
from fastapi import Depends, HTTPException

# 定义依赖：查找商品或返回 404
def get_item_or_404(item_id: int) -> dict:
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="商品不存在")

# 使用依赖
@app.get("/items/{item_id}")
async def get_item(item: dict = Depends(get_item_or_404)):
    return item

@app.put("/items/{item_id}")
async def update_item(data: ItemUpdate, item: dict = Depends(get_item_or_404)):
    item.update(data.model_dump())
    return item

@app.delete("/items/{item_id}")
async def delete_item(item: dict = Depends(get_item_or_404)):
    items_db.remove(item)
    return {"message": "已删除"}
```

### 8.3 `Depends()` 是怎么工作的？

以 `@app.get("/items/{item_id}")` 为例，当用户访问 `/items/3` 时：

```
1. FastAPI 看到参数 item: dict = Depends(get_item_or_404)
2. FastAPI 发现这是一个依赖，于是调用 get_item_or_404()
3. 但 get_item_or_404 需要 item_id 参数
4. FastAPI 从路径参数 {item_id} 中取出值 "3"，传给 get_item_or_404(item_id=3)
5. get_item_or_404 执行后返回一个字典（或抛出 404 异常）
6. FastAPI 把返回值赋给路由函数的 item 参数
7. 最后执行你的路由函数代码
```

**关键点**：`Depends()` 中的函数（如 `get_item_or_404`）本身也可以声明参数，FastAPI 会自动解析这些参数的来源（路径参数、查询参数等），和解析路由函数参数的方式完全一样。

### 8.4 用类做依赖——分页的例子

函数作为依赖适合"做一件事"的场景。如果你需要一组相关的参数（比如分页参数），用**类**更合适：

```python
from fastapi import Depends, Query

class PaginationParams:
    """通用的分页参数依赖。"""
    def __init__(
        self,
        offset: int = Query(ge=0, default=0, description="跳过的记录数"),
        limit: int = Query(ge=1, le=100, default=10, description="返回的最大数量"),
    ):
        self.offset = offset
        self.limit = limit
```

逐行解读：
- 这是一个普通 Python 类，`__init__` 的参数就是依赖的参数
- 参数中可以正常使用 `Query()` 来添加验证规则
- FastAPI 会自动实例化这个类（调用 `__init__`，从请求中提取参数）

在路由中使用：

```python
@app.get("/items")
async def list_items(pagination: PaginationParams = Depends()):
    start = pagination.offset
    end = start + pagination.limit
    return items[start:end]

@app.get("/orders")
async def list_orders(pagination: PaginationParams = Depends()):
    # 复用同样的分页逻辑，不用重复写 offset/limit 参数！
    start = pagination.offset
    end = start + pagination.limit
    return orders[start:end]
```

### 8.5 `Depends()` 的两种写法

```python
# 写法一：明确传入依赖函数/类
item: dict = Depends(get_item_or_404)

# 写法二：省略参数（仅用于类依赖）
pagination: PaginationParams = Depends()
```

**写法二为什么能省略参数？** 因为 FastAPI 会从类型注解 `PaginationParams` 推断出要实例化的类。`Depends()` 等价于 `Depends(PaginationParams)`。

### 8.6 依赖可以嵌套（子依赖）

依赖的参数本身也可以依赖其他东西。这叫"子依赖"：

```python
# 依赖 A：获取查询参数
def query_params(q: str | None = None):
    return {"q": q}

# 依赖 B：依赖 A 的结果
def search_with_query(params: dict = Depends(query_params)):
    # params 就是 query_params 的返回值
    return f"搜索: {params['q']}"

# 路由：依赖 B
@app.get("/search")
async def search(result: str = Depends(search_with_query)):
    return {"result": result}
```

执行链：`query_params` → `search_with_query` → 路由函数。FastAPI 会自动按依赖顺序执行。

### 8.7 依赖注入常见用途

| 用途             | 说明                                                |
| ---------------- | --------------------------------------------------- |
| **复用参数逻辑** | 分页参数、排序参数等，多个路由共用                  |
| **查找资源**     | "根据 ID 查找，找不到就 404"                        |
| **数据库连接**   | 每个请求获取数据库连接，用完自动关闭                |
| **认证/权限**    | "验证 token → 获取当前用户"，所有需要登录的路由共用 |
| **日志/计时**    | 请求前记录开始时间，请求后计算耗时                  |

### 8.8 依赖注入小结

| 概念         | 说明                                               |
| ------------ | -------------------------------------------------- |
| **是什么**   | 把公共逻辑提取出来，FastAPI 自动调用并传结果给路由 |
| **为什么用** | 避免重复代码，逻辑集中管理，改一处生效全部         |
| **怎么用**   | 函数参数写 `= Depends(函数或类)`                   |
| **函数依赖** | 适合"做一件事"（查找资源、获取数据库连接）         |
| **类依赖**   | 适合"一组参数"（分页参数、排序参数）               |
| **嵌套依赖** | 依赖可以依赖其他依赖，形成链条                     |

---

## 9. 错误处理 HTTPException

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id > len(items_db):
        raise HTTPException(status_code=404, detail="商品不存在")
    return items_db[item_id]
```

`HTTPException` 是 FastAPI 用来返回 HTTP 错误的方式：
- `status_code`：HTTP 状态码（如 404）
- `detail`：错误描述信息，会以 JSON 形式返回给客户端

返回的响应：
```json
{"detail": "商品不存在"}
```

### 常见 HTTP 状态码

| 状态码 | 含义     | 何时使用                                  |
| ------ | -------- | ----------------------------------------- |
| 200    | 成功     | 默认返回值                                |
| 201    | 已创建   | POST 创建资源成功                         |
| 400    | 请求错误 | 客户端发送了无效数据                      |
| 401    | 未认证   | 需要登录但没有提供 token                  |
| 403    | 禁止访问 | 没有权限                                  |
| 404    | 未找到   | 资源不存在                                |
| 422    | 验证失败 | FastAPI 自动返回（数据类型/验证不通过时） |

---

## 10. CORS 跨域配置

前端（如 React/Vue）和后端在不同端口时，浏览器会阻止跨域请求。需要配置 CORS（跨域资源共享）：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允许的前端地址
    allow_credentials=True,                    # 允许携带 Cookie
    allow_methods=["*"],   # 允许所有 HTTP 方法
    allow_headers=["*"],   # 允许所有请求头
)
```

- `allow_origins`：允许哪些前端地址访问。`["*"]` 表示允许所有来源
- `allow_methods`：允许哪些 HTTP 方法。`["*"]` 表示 GET、POST、PUT、DELETE 等全部允许
- `allow_headers`：允许哪些请求头

> 开发时可以用 `allow_origins=["*"]` 允许所有来源，但**生产环境不要这么做**。

---

## 11. 完整 CRUD 示例

配套代码 `fastapi_demo.py` 是一个完整的商品管理 API，包含：

| 操作     | 方法   | 路径               | 说明                   |
| -------- | ------ | ------------------ | ---------------------- |
| 列表     | GET    | `/items`           | 支持分页               |
| 搜索     | GET    | `/items/search`    | 关键词、价格范围、标签 |
| 详情     | GET    | `/items/{item_id}` | 单个商品               |
| 创建     | POST   | `/items`           | 新增商品               |
| 更新     | PUT    | `/items/{item_id}` | 完整更新               |
| 部分更新 | PATCH  | `/items/{item_id}` | 只改部分字段           |
| 删除     | DELETE | `/items/{item_id}` | 删除商品               |

### 运行步骤

```powershell
cd 04-tools-and-frameworks/fastapi
uv add fastapi uvicorn pydantic
uv run python -m uvicorn fastapi_demo:app --reload
```

然后：
1. 打开 **http://127.0.0.1:8000/docs** 查看交互式文档
2. 在文档页面上直接点击 **"Try it out"** 测试每个 API
3. 也可以用 curl 测试：

```powershell
# 获取商品列表
curl http://127.0.0.1:8000/items

# 搜索商品
curl "http://127.0.0.1:8000/items/search?keyword=Python&min_price=10"

# 创建商品
curl -X POST http://127.0.0.1:8000/items -H "Content-Type: application/json" -d "{\"name\":\"鼠标\",\"price\":99.0}"

# 获取单个商品
curl http://127.0.0.1:8000/items/1

# 部分更新
curl -X PATCH http://127.0.0.1:8000/items/1 -H "Content-Type: application/json" -d "{\"price\":49.9}"

# 删除
curl -X DELETE http://127.0.0.1:8000/items/1
```

---

## 12. 项目结构建议

小项目单文件就够了，当项目变大时，推荐这样组织：

```
my_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 实例、中间件、启动事件
│   ├── models.py        # Pydantic 模型
│   ├── dependencies.py  # 依赖注入函数
│   ├── routers/
│   │   ├── items.py     # 商品相关路由
│   │   └── users.py     # 用户相关路由
│   └── database.py      # 数据库连接
├── pyproject.toml
└── README.md
```

### 使用 APIRouter 拆分路由

当路由越来越多，全部写在 `main.py` 会变得难以维护。FastAPI 提供 `APIRouter` 来把路由按功能分组：

```python
# app/routers/items.py
from fastapi import APIRouter

# 创建路由器，prefix 是公共前缀，tags 用于 API 文档分组
router = APIRouter(prefix="/items", tags=["商品"])

@router.get("/")
async def list_items():
    ...

@router.get("/{item_id}")
async def get_item(item_id: int):
    ...

# app/main.py
from fastapi import FastAPI
from app.routers import items

app = FastAPI()
# 把 items 路由器注册到主应用
app.include_router(items.router)
```

- `prefix="/items"` —— 这个路由器下所有路由自动加上 `/items` 前缀
- `tags=["商品"]` —— 在 `/docs` 文档页面中，这些路由会归到"商品"分组
- `app.include_router()` —— 把路由器注册到主应用

---

## 13. FastAPI + Pydantic 协作流程

这是 FastAPI 处理一个请求的完整流程：

```
客户端发送 JSON 请求
        ↓
FastAPI 接收请求，提取参数
        ↓
Pydantic 验证数据（类型、约束、自定义验证器）
        ↓  验证失败 → 返回 422 错误（自动）
        ↓  验证成功 ↓
执行路由函数（你的代码）
        ↓
response_model 格式化响应
        ↓
返回 JSON 给客户端
```

---

## 速查表

| 功能               | 代码                                             |
| ------------------ | ------------------------------------------------ |
| 创建应用           | `app = FastAPI()`                                |
| GET 路由           | `@app.get("/path")`                              |
| POST 路由          | `@app.post("/path")`                             |
| 路径参数           | `@app.get("/items/{id}")` + `id: int`            |
| 查询参数（简单）   | `keyword: str = ""`                              |
| 查询参数（带验证） | `keyword: str = Query(default="", min_length=1)` |
| 请求体             | `item: ItemCreate`（Pydantic 模型参数）          |
| 响应模型           | `@app.get(..., response_model=ItemResponse)`     |
| 依赖注入（函数）   | `item: dict = Depends(get_item_or_404)`          |
| 依赖注入（类）     | `pagination: PaginationParams = Depends()`       |
| 抛出错误           | `raise HTTPException(status_code=404)`           |
| CORS               | `app.add_middleware(CORSMiddleware, ...)`        |
| 路由拆分           | `APIRouter(prefix="/items")`                     |
| 运行               | `uvicorn main:app --reload`                      |
| 交互式文档         | `/docs`                                          |
| 另一种文档         | `/redoc`                                         |
