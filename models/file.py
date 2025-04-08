from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime
from .database import Base

# class File(Base):
#     __tablename__ = "files"

#     id = Column(Integer, primary_key=True, index=True)
#     knowledge_id = Column(Integer, ForeignKey("knowledges.id"))
#     file_name = Column(String(255))
#     content_type = Column(String(255))
#     file_data = Column(LargeBinary)
#     uploaded_at = Column(DateTime, default=datetime.utcnow)

#     # リレーションシップ
#     knowledge = relationship("Knowledge", back_populates="files") 

# テーブル定義との整合・記法の変更・マージ　0407
class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    knowledge_id: Mapped[int] = mapped_column(Integer, ForeignKey("knowledges.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(255))
    file_data: Mapped[bytes] = mapped_column(LargeBinary)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    # リレーションシップ
    knowledge = relationship("Knowledge", back_populates="files")