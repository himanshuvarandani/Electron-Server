from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.models.base import Base
from app.database.models.classes import Classes


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    email = Column(String(30), unique=True)
    faculty_no = Column(String(30), unique=True)
    enroll_no = Column(String(30), unique=True)
    department_name = Column(String(30))
    class_id = Column(Integer, ForeignKey(Classes.id))
    password_hash = Column(String(512))
