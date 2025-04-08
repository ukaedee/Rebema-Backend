from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime
from .database import Base

# class UserActivity(Base):
#     __tablename__ = "user_activities"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     action = Column(String(50))  # 例: "create_knowledge", "comment", "view"
#     xp_amount = Column(Integer)
#     timestamp = Column(DateTime, default=datetime.utcnow)

#     # リレーションシップ
#     user = relationship("User", back_populates="activities") 

# テーブル定義との整合・記法の変更・マージ　0407
class UserActivity(Base):
    __tablename__ = "user_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(50))  # 例: "create_knowledge", "comment", "view"
    xp_amount: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    # リレーションシップ
    user = relationship("User", back_populates="activities")