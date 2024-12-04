from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from auth.schemas import TokenData
from auth.models import User
from jose import JWTError, jwt
from sqlmodel import select
import os
from dotenv import load_dotenv

load_dotenv(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 2000


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return user


async def authenticate_user(session, username: str, password: str):
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(session: AsyncSession, token: str = Depends(oauth_2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def create_user(session: AsyncSession, user_data):
    if user_data.password1 != user_data.password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )
    # Check if email exists
    email_query = await session.execute(select(User).where(User.email == user_data.email))
    existing_email = email_query.one_or_none()  # Fixed method
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username exists
    username_query = await session.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_username = username_query.one_or_none()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password1),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    session.add(user)
    await session.commit()
    return user
