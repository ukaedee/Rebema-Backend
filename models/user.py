from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from .knowledge_collaborator import KnowledgeCollaborator 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    username = Column(String(255), unique=True, index=True)
    level = Column(Integer, default=1)
    points = Column(Integer, default=0)
    current_xp = Column(Integer, default=0)
    experience_points = Column(Integer, default=0)
    is_first_login = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    avatar_data = Column(LargeBinary, nullable=True)
    avatar_content_type = Column(String(50), nullable=True)  # 画像のMIMEタイプを保存
    department = Column(String(100), nullable=True)

    # リレーションシップ
    knowledges = relationship("Knowledge", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    activities = relationship("UserActivity", back_populates="user")
    collaborations = relationship("KnowledgeCollaborator", back_populates="user")
    profile = relationship("Profile", back_populates="user", uselist=False) 

    @property
    def avatar_url(self) -> str | None:
        """
        ユーザーのアバター画像のURLを返す
        画像が設定されていない場合はNoneを返す
        """
        if self.avatar_data is None:
            return None
        return f"/profile/{self.id}/avatar"


