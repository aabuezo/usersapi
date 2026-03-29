from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    email: EmailStr = Field(..., min_length=5)
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)


class UserUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=3)
    last_name: str | None = Field(None, min_length=3)
    email: EmailStr | None = Field(None, min_length=5)
    username: str | None = Field(None, min_length=3)
    password: str | None = Field(None, min_length=4)


class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    username: str


class UserLogin(BaseModel):
    username: str
    password: str
