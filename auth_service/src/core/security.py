from datetime import datetime, timedelta
from typing import Union

from passlib.context import CryptContext
from jose import JWTError, jwt

from src.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

assert JWT_SECRET_KEY is not None, "JWT_SECRET_KEY is not set"
assert JWT_ALGORITHM is not None, "JWT_ALGORITHM is not set"
assert JWT_EXPIRE_MINUTES is not None, "JWT_EXPIRE_MINUTES is not set"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_jwt
    except JWTError:
        return None