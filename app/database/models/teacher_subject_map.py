from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.models.base import Base
from app.database.models.subjects import Subjects
from app.database.models.teachers import Teachers


class TeacherSubjectMap(Base):
    __tablename__ = "teacher_subject_map"
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey(Teachers.id))
    subject_id = Column(Integer, ForeignKey(Subjects.id))
