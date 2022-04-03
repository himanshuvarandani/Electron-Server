from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from app.database.models.base import Base
from app.database.models.subjects import Subjects
from app.database.models.students import Students


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    attendance = Column(Integer)
    subject_id = Column(Integer, ForeignKey(Subjects.id))
    student_id = Column(Integer, ForeignKey(Students.id))
