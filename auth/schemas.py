from pydantic import BaseModel, Field, EmailStr
from dotenv import load_dotenv


class SignUpForm(BaseModel):
    email: EmailStr
    username: str
    password1: str
    password2: str
    first_name: str
    last_name: str


class LoginForm(BaseModel):
    email: str
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
