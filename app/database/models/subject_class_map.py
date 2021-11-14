from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.models.base import Base
from app.database.models.classes import Classes
from app.database.models.subjects import Subjects


class SubjectClassMap(Base):
    __tablename__ = "subject_class_map"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey(Subjects.id))
    class_id = Column(Integer, ForeignKey(Classes.id))
