from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

from models.database import get_db
from models.user import User

# 設定
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # 環境変数から取得、デフォルトも設定
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# パスワードハッシュ
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# トークンエンドポイントのURLを正しく設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# パスワード照合
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# パスワードのハッシュ化
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# アクセストークン作成
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 現在のユーザー取得（JWTトークンから）
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報が正しくありません",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # トークン解凍データの例 {'sub': 'rebema1@example.com', 'exp': 1744215602} 
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise credentials_exception
    return user
