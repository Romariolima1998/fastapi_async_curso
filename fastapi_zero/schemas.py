from pydantic import BaseModel, EmailStr


class MessageOutput(BaseModel):
    message: str


class UserSchemaInput(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaOutput(BaseModel):
    id: int
    username: str
    email: EmailStr


class User_DB(UserSchemaInput):
    id: int


class UserListSchema(BaseModel):
    users: list[UserSchemaOutput]
