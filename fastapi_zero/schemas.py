from pydantic import BaseModel, Field, ConfigDict, EmailStr


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


class Token(BaseModel):
    token_type: str
    access_token: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)