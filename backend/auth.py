#!/usr/bin/env python3
"""Authentication helpers for API endpoints.

Supports OAuth2 password flow with JWT bearer tokens while keeping
legacy compatibility for static bearer token and X-User header clients.
"""
from datetime import datetime, timedelta, timezone
import os
import secrets
from typing import Optional

from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _get_jwt_config() -> tuple[str, str, int]:
    secret_key = os.getenv("JWT_SECRET_KEY", "dev-insecure-change-me")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    expires_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    return secret_key, algorithm, expires_minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_form_user(username: str, password: str) -> Optional[str]:
    configured_username = os.getenv("AUTH_USERNAME")
    configured_password = os.getenv("AUTH_PASSWORD")
    configured_password_hash = os.getenv("AUTH_PASSWORD_HASH")

    if not configured_username or username != configured_username:
        return None

    if configured_password_hash:
        if verify_password(password, configured_password_hash):
            return configured_username
        return None

    if configured_password and secrets.compare_digest(password, configured_password):
        return configured_username

    return None


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    secret_key, algorithm, expires_minutes = _get_jwt_config()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=expires_minutes))
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def _decode_jwt_subject(token: str) -> Optional[str]:
    secret_key, algorithm, _ = _get_jwt_config()
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        subject = payload.get("sub")
        if isinstance(subject, str) and subject:
            return subject
        return None
    except JWTError:
        return None


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    x_user: Optional[str] = Header(default=None, alias="X-User"),
) -> str:
    if token:
        jwt_subject = _decode_jwt_subject(token)
        if jwt_subject:
            return jwt_subject

        configured_token = os.getenv("API_BEARER_TOKEN")
        token_subject = os.getenv("API_BEARER_SUBJECT", "token_user")
        if configured_token and secrets.compare_digest(token, configured_token):
            return token_subject

        raise HTTPException(status_code=401, detail="Invalid bearer token")

    if x_user:
        return x_user

    raise HTTPException(status_code=401, detail="Authentication required: provide X-User or Bearer token")
