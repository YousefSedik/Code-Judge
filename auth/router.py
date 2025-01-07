from fastapi.routing import APIRouter
from auth.schemas import LoginForm, SignUpForm
from dotenv import load_dotenv
from auth.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from auth.utils import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_user,
    get_current_user,
)
from db import get_session
from auth.models import User
from datetime import timedelta, datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv("../.env")

router = APIRouter()


@router.post("/register")
async def register(
    SignUpForm: SignUpForm, session: AsyncSession = Depends(get_session)
):

    await create_user(session, SignUpForm)
    return {"created": True}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    token,
    session: AsyncSession = Depends(get_session),
):

    user = await get_current_user(session, token)
    return {"username": user.username, "email": user.email}
