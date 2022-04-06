from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.models.base import Base
from app.database.models.classes import Classes


class Subjects(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    name = Column(String(100))
