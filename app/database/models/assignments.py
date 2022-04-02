from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from app.database.models.base import Base
from app.database.models.subjects import Subjects
from app.database.models.teachers import Teachers


class Assignments(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    body = Column(String(120))
    attachement = Column(String(300))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    subject_id = Column(Integer, ForeignKey(Subjects.id))
    teacher_id = Column(Integer, ForeignKey(Teachers.id))
