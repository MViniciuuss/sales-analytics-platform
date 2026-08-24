import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from pwdlib import PasswordHash
from sqlalchemy import text

from backend.app.database import engine


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)

password_manager = PasswordHash.recommended()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"


class LoginRequest(BaseModel):
    email: str
    password: str


def create_access_token(user_id: int, email: str):
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET não configurado.")

    expiration = datetime.now(timezone.utc) + timedelta(hours=8)

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


@router.post("/login")
def login(credentials: LoginRequest):
    query = text(
        """
        SELECT
            id,
            full_name,
            email,
            password_hash,
            is_active
        FROM users
        WHERE email = :email
        LIMIT 1
        """
    )

    with engine.connect() as connection:
        user = connection.execute(
            query,
            {"email": credentials.email.lower()},
        ).mappings().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário desativado.",
        )

    password_is_valid = password_manager.verify(
        credentials.password,
        user["password_hash"],
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    token = create_access_token(
        user_id=user["id"],
        email=user["email"],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["full_name"],
            "email": user["email"],
        },
    }