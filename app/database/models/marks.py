from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.models.base import Base
from app.database.models.assignments import Assignments
from app.database.models.students import Students
from app.database.models.teachers import Teachers


class Marks(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Students.id))
    teacher_id = Column(Integer, ForeignKey(Teachers.id))
    assignment_id = Column(Integer, ForeignKey(Assignments.id))
    marks = Column(Integer)
