from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from app.database.models.base import Base
from app.database.models.subjects import Subjects
from app.database.models.teachers import Teachers


class Announcements(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    body = Column(String(120))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    subject_id = Column(Integer, ForeignKey(Subjects.id))
    teacher_id = Column(Integer, ForeignKey(Teachers.id))
