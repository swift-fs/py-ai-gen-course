"""
第 Py-01 章配套代码：Pydantic 数据验证
运行方式：uv add pydantic && uv run python pydantic_demo.py
"""

from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)


# ============================================================
# 1. 快速上手：第一个 Pydantic 模型
# ============================================================
print("=" * 50)
print("1. 快速上手：第一个 Pydantic 模型")
print("=" * 50)


class User(BaseModel):
    """最简单的 Pydantic 模型——定义字段名和类型即可。"""

    id: int
    name: str
    email: str
    age: int = 0  # 带默认值的字段（可选字段）


# 用关键字参数创建
user1 = User(id=1, name="小明", email="xm@example.com", age=18)
print(f"  user1: {user1}")
print(f"  user1.name: {user1.name}")
print(f"  user1.age: {user1.age}")

# 用字典解包创建（常见于读取 JSON / 数据库数据）
data = {"id": 2, "name": "小红", "email": "xh@example.com"}
user2 = User(**data)
print(f"  user2（使用默认 age）: {user2}")


# ============================================================
# 2. 自动类型转换
# ============================================================
print("\n" + "=" * 50)
print("2. 自动类型转换")
print("=" * 50)

# Pydantic 会尽可能帮你把数据"转换"成目标类型
# 这在处理表单数据、API 请求时特别有用
user3 = User(id="3", name="小刚", email="xg@example.com", age="20")
print(f"  id='3' → {user3.id!r} (类型: {type(user3.id).__name__})")
print(f"  age='20' → {user3.age!r} (类型: {type(user3.age).__name__})")


# ============================================================
# 3. 验证错误：友好的错误提示
# ============================================================
print("\n" + "=" * 50)
print("3. 验证错误：友好的错误提示")
print("=" * 50)

try:
    User(id="not_a_number", name="测试", email="test@example.com")
except ValidationError as error:
    print("  验证失败！错误信息：")
    for err in error.errors():
        print(f"    字段: {'.'.join(str(loc) for loc in err['loc'])}")
        print(f"    错误: {err['msg']}")
        print(f"    输入: {err['input']!r}")
        print()


# ============================================================
# 4. Field —— 给字段加约束和元信息
# ============================================================
print("=" * 50)
print("4. Field —— 给字段加约束和元信息")
print("=" * 50)


class Product(BaseModel):
    """使用 Field 为字段添加验证约束和描述信息。"""

    name: str = Field(min_length=1, max_length=100, description="商品名称")
    price: float = Field(gt=0, description="商品价格，必须大于 0")
    stock: int = Field(ge=0, description="库存数量，不能为负数")
    tags: list[str] = Field(default_factory=list, description="标签列表")


# 合法数据
product = Product(name="Python 书", price=59.9, stock=100, tags=["编程", "入门"])
print(f"  合法商品: {product}")

# 非法数据演示
print("  --- 尝试创建非法商品 ---")
for bad_data, desc in [
    ({"name": "", "price": 59.9, "stock": 10}, "名称为空"),
    ({"name": "书", "price": -1, "stock": 10}, "价格为负"),
    ({"name": "书", "price": 59.9, "stock": -5}, "库存为负"),
]:
    try:
        Product(**bad_data)
    except ValidationError as error:
        print(f"  [{desc}] → 错误: {error.errors()[0]['msg']}")


# ============================================================
# 5. 可选字段与默认值
# ============================================================
print("\n" + "=" * 50)
print("5. 可选字段与默认值")
print("=" * 50)


class Article(BaseModel):
    title: str
    content: str
    author: str = "匿名"
    published_at: Optional[datetime] = None
    tags: list[str] = Field(default_factory=list)


article = Article(title="Pydantic 入门", content="Pydantic 是...")
print(f"  author 默认值: {article.author!r}")
print(f"  published_at 默认值: {article.published_at!r}")
print(f"  tags 默认值: {article.tags!r}")


# ============================================================
# 6. 自定义验证器
# ============================================================
print("\n" + "=" * 50)
print("6. 自定义验证器")
print("=" * 50)


class SignupForm(BaseModel):
    """演示 field_validator 和 model_validator 的用法。"""

    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    password_confirm: str

    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("用户名只能包含字母和数字")
        return value

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:
        if not any(char.isdigit() for char in value):
            raise ValueError("密码必须包含至少一个数字")
        if not any(char.isupper() for char in value):
            raise ValueError("密码必须包含至少一个大写字母")
        return value

    @model_validator(mode="after")
    def passwords_match(self) -> "SignupForm":
        if self.password != self.password_confirm:
            raise ValueError("两次输入的密码不一致")
        return self


# 合法注册
form = SignupForm(
    username="xiaoming123",
    password="SecurePass1",
    password_confirm="SecurePass1",
)
print(f"  注册成功: {form.username}")

# 非法注册演示
print("  --- 尝试非法注册 ---")
for bad_data, desc in [
    (
        {
            "username": "xm!",
            "password": "SecurePass1",
            "password_confirm": "SecurePass1",
        },
        "用户名含特殊字符",
    ),
    (
        {
            "username": "xiaoming",
            "password": "weakpass",
            "password_confirm": "weakpass",
        },
        "密码太弱",
    ),
    (
        {
            "username": "xiaoming",
            "password": "SecurePass1",
            "password_confirm": "Different1",
        },
        "密码不一致",
    ),
]:
    try:
        SignupForm(**bad_data)
    except ValidationError as error:
        print(f"  [{desc}] → {error.errors()[0]['msg']}")


# ============================================================
# 7. 嵌套模型
# ============================================================
print("\n" + "=" * 50)
print("7. 嵌套模型")
print("=" * 50)


class Address(BaseModel):
    city: str
    district: str
    street: str = ""


class Order(BaseModel):
    order_id: int
    customer_name: str
    items: list[str]
    shipping_address: Address  # 嵌套另一个 Pydantic 模型


order = Order(
    order_id=1001,
    customer_name="小明",
    items=["Python 书", "键盘"],
    shipping_address={"city": "北京", "district": "海淀区", "street": "中关村大街1号"},
)
print(f"  订单: {order.order_id}, 客户: {order.customer_name}")
print(f"  商品: {order.items}")
print(f"  收货地址: {order.shipping_address.city} {order.shipping_address.district}")


# ============================================================
# 8. 序列化：把模型转回字典 / JSON
# ============================================================
print("\n" + "=" * 50)
print("8. 序列化：把模型转回字典 / JSON")
print("=" * 50)

# 转为 Python 字典
dump_dict = user1.model_dump()
print(f"  model_dump(): {dump_dict}")

# 转为 JSON 字符串
dump_json = user1.model_dump_json()
print(f"  model_dump_json(): {dump_json}")

# 只导出部分字段
partial = user1.model_dump(include={"name", "email"})
print(f"  只导出 name 和 email: {partial}")

# 排除部分字段
excluded = user1.model_dump(exclude={"id"})
print(f"  排除 id: {excluded}")


# ============================================================
# 9. model_validate：从字典 / JSON 创建模型
# ============================================================
print("\n" + "=" * 50)
print("9. model_validate：从字典 / JSON 创建模型")
print("=" * 50)

json_str = '{"id": 5, "name": "小华", "email": "xh@test.com", "age": 22}'

# 从 JSON 字符串直接创建
user_from_json = User.model_validate_json(json_str)
print(f"  从 JSON 创建: {user_from_json}")

# 从字典创建（和 User(**data) 类似，但更灵活）
user_from_dict = User.model_validate({"id": 6, "name": "小李", "email": "xl@test.com"})
print(f"  从字典创建: {user_from_dict}")


# ============================================================
# 10. computed_field —— 计算字段
# ============================================================
print("\n" + "=" * 50)
print("10. computed_field —— 计算字段")
print("=" * 50)


class Rectangle(BaseModel):
    width: float = Field(gt=0)
    height: float = Field(gt=0)

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

    @computed_field
    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


rect = Rectangle(width=5, height=3)
print(f"  矩形: {rect.width} x {rect.height}")
print(f"  面积: {rect.area}")
print(f"  周长: {rect.perimeter}")
print(f"  model_dump 包含计算字段: {rect.model_dump()}")


# ============================================================
# 11. model_config —— 模型配置
# ============================================================
print("\n" + "=" * 50)
print("11. model_config —— 模型配置")
print("=" * 50)


class FlexibleModel(BaseModel):
    """演示常用的模型配置选项。"""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="forbid",
    )

    name: str
    age: int


# 字符串自动去除首尾空格
flex = FlexibleModel(name="  小明  ", age=18)
print(f"  自动去除空格: name={flex.name!r}")

# 禁止传入多余字段
print("  --- 尝试传入多余字段 ---")
try:
    FlexibleModel(name="小明", age=18, extra_field="不允许")
except ValidationError as error:
    print(f"  错误: {error.errors()[0]['msg']}")


# ============================================================
# 12. TypeAdapter —— 验证任意类型
# ============================================================
print("\n" + "=" * 50)
print("12. TypeAdapter —— 验证任意类型")
print("=" * 50)

# 不需要创建 BaseModel，也能验证数据
list_adapter = TypeAdapter(list[int])
result = list_adapter.validate_python(["1", "2", "3"])
print(f"  验证 list[int]: {result} (类型: {[type(x).__name__ for x in result]})")

dict_adapter = TypeAdapter(dict[str, float])
result2 = dict_adapter.validate_python({"pi": "3.14", "e": "2.72"})
print(f"  验证 dict[str, float]: {result2}")


# ============================================================
# 13. 模型继承与组合
# ============================================================
print("\n" + "=" * 50)
print("13. 模型继承与组合")
print("=" * 50)


class EmployeeBase(BaseModel):
    """基础员工信息——可用于创建、更新、返回等不同场景。"""

    name: str
    department: str


class EmployeeCreate(EmployeeBase):
    """创建员工时的模型（需要额外信息）。"""

    email: str  # 安装 email-validator 后可用 EmailStr 做邮箱格式验证


class EmployeePublic(EmployeeBase):
    """返回给前端时的模型（包含 id，不包含敏感信息）。"""

    id: int


class EmployeeUpdate(BaseModel):
    """更新员工时的模型（所有字段都是可选的）。"""

    name: str | None = None
    department: str | None = None
    email: str | None = None  # 安装 email-validator 后可用 EmailStr


# 创建
new_employee = EmployeeCreate(name="小明", department="工程部", email="xm@company.com")
print(f"  创建: {new_employee}")

# 转换为"公开"模型（模拟从数据库返回）
public = EmployeePublic(id=1, **new_employee.model_dump(exclude={"email"}))
print(f"  公开: {public}")

# 部分更新
update_data = {"department": "产品部"}
update = EmployeeUpdate(**update_data)
print(f"  更新: {update}")


# ============================================================
# 14. 实战案例：完整的 API 数据模型
# ============================================================
print("\n" + "=" * 50)
print("14. 实战案例：博客系统的数据模型")
print("=" * 50)


class BlogPostCreate(BaseModel):
    """创建博客文章的请求体。"""

    title: str = Field(min_length=1, max_length=200, description="文章标题")
    content: str = Field(min_length=10, description="文章内容，至少 10 个字符")
    tags: list[str] = Field(
        default_factory=list, max_length=5, description="标签，最多 5 个"
    )

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, tags: list[str]) -> list[str]:
        # 去重、去空、转小写
        seen: set[str] = set()
        result: list[str] = []
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in seen:
                seen.add(tag)
                result.append(tag)
        return result


class BlogPost(BlogPostCreate):
    """完整的博客文章模型（含系统生成的字段）。"""

    id: int
    author: str
    created_at: datetime = Field(default_factory=datetime.now)
    likes: int = 0

    @computed_field
    @property
    def summary(self) -> str:
        return self.content[:50] + "..." if len(self.content) > 50 else self.content


# 创建一篇博客
post = BlogPost(
    id=1,
    author="小明",
    title="Pydantic 入门指南",
    content="Pydantic 是 Python 中最流行的数据验证库，它使用类型注解来定义数据结构...",
    tags=["Python", "pydantic", "tutorial"],
)
print(f"  文章 ID: {post.id}")
print(f"  标题: {post.title}")
print(f"  作者: {post.author}")
print(f"  标签: {post.tags}")
print(f"  摘要: {post.summary}")
print(f"  序列化（排除 content）: {post.model_dump(exclude={'content'})}")


print("\n" + "=" * 50)
print("所有演示完成！")
print("=" * 50)
