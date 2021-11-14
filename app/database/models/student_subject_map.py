from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.models.base import Base
from app.database.models.subjects import Subjects
from app.database.models.students import Students


class StudentSubjectMap(Base):
    __tablename__ = "student_subject_map"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Students.id))
    subject_id = Column(Integer, ForeignKey(Subjects.id))
