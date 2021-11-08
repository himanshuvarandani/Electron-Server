from sqlalchemy import Column, Integer, String
from app.database.models.base import Base


class Classes(Base):
  __tablename__ = "classes"
  id = Column(Integer, primary_key=True)
  name = Column(String(30))
  year = Column(Integer)
  department_name = Column(String(30))
