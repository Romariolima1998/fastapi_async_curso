from pydantic import BaseModel, EmailStr, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)


class User_DB(UserSchemaInput):
    id: int


class UserListSchema(BaseModel):
    users: list[UserSchemaOutput]
