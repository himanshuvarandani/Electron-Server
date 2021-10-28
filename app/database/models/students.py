from sqlalchemy import Column, Integer, String
from app.database.models.base import Base


class Students(Base):
  __tablename__ = "students"
  id = Column(Integer, primary_key=True)
  name = Column(String(30))
  email = Column(String(30), unique=True)
  password_hash = Column(String(512))
