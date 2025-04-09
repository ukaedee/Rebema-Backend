from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import EmailStr

from models.database import get_db
from models.user import User
from core.security import (
    verify_password,
    create_access_token,
    get_current_user
)

# ⬇️ この中にカスタムフォームクラスを直接定義（utilsに分けてもOK）
class OAuth2EmailRequestForm:
    def __init__(
        self,
        email: EmailStr = Form(..., description="ログイン用のメールアドレス"),
        password: str = Form(..., description="ログイン用のパスワード"),
    ):
        self.username = email  # FastAPI互換のため
        self.password = password
        self.scopes = []
        self.client_id = None
        self.client_secret = None


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login")
async def login(
    form_data: OAuth2EmailRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print("ログイン試行:", form_data.username)  # emailが入る

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        print("ユーザーが存在しません")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
        )

    if not verify_password(form_data.password, user.password_hash):
        print("パスワードが一致しません")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"jwt_token": access_token}


@router.get("/me")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.username,
        "department": current_user.department,
        "level": current_user.level,
        "experiencePoints": current_user.experience_points,
    }
