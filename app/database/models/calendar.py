from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from app.database.models.base import Base
from app.database.models.subjects import Subjects
from app.database.models.classes import Classes


class Calendar(Base):
    __tablename__ = "calendar"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey(Subjects.id))
    class_id = Column(String(30), ForeignKey(Classes.name))
    deadline = Column(DateTime)
    task = Column(String(200))
