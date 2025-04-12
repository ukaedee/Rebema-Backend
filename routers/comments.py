from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from models.database import get_db
from models.user import User
from models.knowledge import Knowledge
from models.comment import Comment
from core.security import get_current_user
from pydantic import BaseModel
from fastapi import Path
from typing import Optional, List

router = APIRouter(prefix="/knowledge/{knowledge_id}/comments", tags=["comments"])

# コメントのリクエストモデル
class CommentCreate(BaseModel):
    content: str

# コメントのレスポンスモデル
class CommentResponse(BaseModel):
    id: int
    content: str
    author_id: int
    author_name: str
    avatar_url: Optional[str]
    created_at: datetime

# コメントを作成
@router.post("/", response_model=CommentResponse)
async def create_comment(
    knowledge_id: int = Path(..., description="コメント対象のナレッジID"),
    comment: CommentCreate = Body(..., description="コメントの内容"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="ナレッジが見つかりません")

    new_comment = Comment(
        knowledge_id=knowledge_id,
        content=comment.content,
        author_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return CommentResponse(
        id=new_comment.id,
        content=new_comment.content,
        author_id=current_user.id,
        author_name=current_user.username,
        avatar_url=current_user.avatar_url,
        created_at=new_comment.created_at
    )

# コメント一覧を取得
@router.get("/", response_model=List[CommentResponse])
async def get_comments(
    knowledge_id: int,
    db: Session = Depends(get_db)
):
    # authorをeager loadして取得
    comments = db.query(Comment).options(
        joinedload(Comment.author)
    ).filter(Comment.knowledge_id == knowledge_id).order_by(Comment.created_at.asc()).all()

    return [
        CommentResponse(
            id=comment.id,
            content=comment.content,
            author_id=comment.author_id,
            # authorがNoneの場合のフォールバック
            author_name=comment.author.username if comment.author else "削除されたユーザー",
            avatar_url=comment.author.avatar_url if comment.author else None,
            created_at=comment.created_at
        )
        for comment in comments
    ]

# コメントを削除
@router.delete("/{comment_id}")
async def delete_comment(
    knowledge_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.knowledge_id == knowledge_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="コメントが見つかりません")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="コメントを削除する権限がありません")

    db.delete(comment)
    db.commit()

    return {"detail": "コメントが削除されました"}
