from pydantic import BaseModel, Field, EmailStr


class UserRequestAdd(BaseModel):
    username: str | None = Field(None)
    password: str
    email: EmailStr


class UserAdd(BaseModel):
    username: str | None = Field(None)
    hashed_password: str
    email: EmailStr


class User(BaseModel):
    id: int
    username: str | None = Field(None)
    email: EmailStr
