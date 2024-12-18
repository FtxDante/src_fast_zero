from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class FiltersPage(BaseModel):
    offset: int = 0
    limit: int = 100


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterTodo(FiltersPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
