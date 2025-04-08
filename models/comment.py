from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime
from .database import Base

# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     knowledge_id = Column(Integer, ForeignKey("knowledges.id"))
#     content = Column(Text)
#     author_id = Column(Integer, ForeignKey("users.id"))
#     created_at = Column(DateTime, default=datetime.utcnow)

#     # リレーションシップ
#     knowledge = relationship("Knowledge", back_populates="comments")
#     author = relationship("User", back_populates="comments") 

# テーブル定義との整合・記法の変更・マージ　0407
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    knowledge_id: Mapped[int] = mapped_column(Integer, ForeignKey("knowledges.id"))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    # リレーションシップ
    knowledge = relationship("knowledge", back_populates="comments")
    author = relationship("User", back_populates="comments")