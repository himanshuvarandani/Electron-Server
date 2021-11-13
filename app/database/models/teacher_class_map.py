from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.models.base import Base
from app.database.models.classes import Classes
from app.database.models.teachers import Teachers


class TeacherClassMap(Base):
  __tablename__ = "teacher_class_map"
  id = Column(Integer, primary_key=True)
  teacher_id = Column(Integer, ForeignKey(Teachers.id))
  class_id = Column(Integer, ForeignKey(Classes.id))
