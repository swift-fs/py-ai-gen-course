from pydantic import BaseModel, ConfigDict, Field, computed_field


class MyUser(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
    )
    name: str = Field(description="用户姓名", min_length=2, max_length=10)
    age: int = Field(description="用户年龄", ge=0, le=120)
    email: str = Field(description="用户邮箱")
    password: str = Field(description="用户密码")
    is_active: bool = Field(description="用户是否激活", default=True)
    is_admin: bool = Field(description="用户是否管理员", default=False)

    @computed_field
    @property
    def description(self) -> str:
        return f"用户 {self.name}，年龄{self.age}，邮箱{self.email}，是否管理员{self.is_admin}，是否激活{self.is_active}"


if __name__ == "__main__":
    user = MyUser(
        name="张三",
        age=30,
        email="zhangsan@example.com",
        password="123456",
    )
    print(user)
    user_dict = {
        "name": "张三",
        "age": "78",
        "email": "zhangsan@example.com",
        "password": "123456",
    }
    print(user_dict)
    user01 = MyUser(**user_dict)
    print(user01)
    user02 = MyUser.model_validate(user_dict)
    print(user02)
    print(f"user02 name: {user02.name}")
    print(f"user02 age: {user02.age}")
    print(f"user02 to dict: {user02.model_dump(include=['name', 'age'])}")
    print(f"user02 to json: {user02.model_dump_json(exclude=['password'])}")
