"""
第 Py-02 章配套代码：FastAPI Web 框架
运行方式：
  uv add fastapi uvicorn
  uv run python -m uvicorn fastapi_demo:app --reload
  然后浏览器打开 http://127.0.0.1:8000/docs 查看自动文档
"""

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="FastAPI 入门示例",
    description="配套课程的 FastAPI 演示项目",
    version="0.1.0",
)


# ============================================================
# 模拟数据库（内存中的列表）
# ============================================================
fake_items_db: list[dict] = [
    {"id": 1, "name": "Python 书", "price": 59.9, "tags": ["编程", "入门"]},
    {"id": 2, "name": "机械键盘", "price": 399.0, "tags": ["外设"]},
    {"id": 3, "name": "显示器", "price": 1999.0, "tags": ["外设", "办公"]},
]


# ============================================================
# Pydantic 模型
# ============================================================
class ItemCreate(BaseModel):
    """创建商品时的请求体。"""

    name: str = Field(min_length=1, max_length=100, description="商品名称")
    price: float = Field(gt=0, description="商品价格，必须大于 0")
    tags: list[str] = Field(default_factory=list, max_length=10, description="标签")

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("商品名称不能为空白")
        return value


class ItemUpdate(BaseModel):
    """更新商品时的请求体（所有字段可选）。"""

    name: str | None = None
    price: float | None = Field(default=None, gt=0)
    tags: list[str] | None = None


class ItemResponse(BaseModel):
    """返回给客户端的商品模型。"""

    id: int
    name: str
    price: float
    tags: list[str]


class MessageResponse(BaseModel):
    """通用的消息响应模型。"""

    message: str


# ============================================================
# 依赖注入：公共查询参数
# ============================================================
class PaginationParams:
    """分页参数依赖。"""

    def __init__(
        self,
        offset: int = Query(ge=0, default=0, description="跳过的记录数"),
        limit: int = Query(ge=1, le=100, default=10, description="返回的最大数量"),
    ):
        self.offset = offset
        self.limit = limit


def get_item_or_404(item_id: int) -> dict:
    """根据 ID 查找商品，找不到则返回 404。"""
    for item in fake_items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"商品 {item_id} 不存在")


# ============================================================
# 路由：基本 CRUD
# ============================================================


@app.get("/", response_model=MessageResponse)
async def root():
    """首页——返回欢迎信息。"""
    return {"message": "欢迎使用 FastAPI 入门示例！访问 /docs 查看交互式文档。"}


@app.get("/items", response_model=list[ItemResponse])
async def list_items(pagination: PaginationParams = Depends()):
    """获取商品列表（支持分页）。"""
    start = pagination.offset
    end = start + pagination.limit
    return fake_items_db[start:end]


@app.get("/items/search", response_model=list[ItemResponse])
async def search_items(
    keyword: Optional[str] = Query(default=None, description="搜索关键词"),
    min_price: Optional[float] = Query(default=None, ge=0, description="最低价格"),
    max_price: Optional[float] = Query(default=None, ge=0, description="最高价格"),
    tag: Optional[str] = Query(default=None, description="按标签筛选"),
    pagination: PaginationParams = Depends(),
):
    """搜索商品（支持关键词、价格范围、标签筛选）。"""
    results = fake_items_db

    if keyword:
        results = [item for item in results if keyword.lower() in item["name"].lower()]

    if min_price is not None:
        results = [item for item in results if item["price"] >= min_price]

    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    if tag:
        results = [item for item in results if tag in item["tags"]]

    start = pagination.offset
    end = start + pagination.limit
    return results[start:end]


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item: dict = Depends(get_item_or_404)):
    """根据 ID 获取单个商品。"""
    return item


@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item_data: ItemCreate):
    """创建新商品。"""
    new_id = max(item["id"] for item in fake_items_db) + 1 if fake_items_db else 1
    new_item = {"id": new_id, **item_data.model_dump()}
    fake_items_db.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_data: ItemUpdate,
    item: dict = Depends(get_item_or_404),
):
    """完整更新商品（提供所有字段）。"""
    update_dict = item_data.model_dump(exclude_unset=True)
    item.update(update_dict)
    return item


@app.patch("/items/{item_id}", response_model=ItemResponse)
async def partial_update_item(
    item_data: ItemUpdate,
    item: dict = Depends(get_item_or_404),
):
    """部分更新商品（只修改提供的字段）。"""
    update_dict = item_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        item[key] = value
    return item


@app.delete("/items/{item_id}", response_model=MessageResponse)
async def delete_item(item: dict = Depends(get_item_or_404)):
    """删除商品。"""
    fake_items_db.remove(item)
    return {"message": f"商品 '{item['name']}' 已删除"}


# ============================================================
# 启动入口（方便直接运行）
# ============================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_demo:app", host="127.0.0.1", port=8000, reload=True)
