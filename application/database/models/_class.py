from sqlalchemy import *
from sqlalchemy.orm import *
from application.database.models import Base

class _Class(Base):
    __tablename__ = "Class"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    year = Column(Date, nullable=False)

    teacher_id = Column(Integer, ForeignKey("Teacher.id"))
    teacher = relationship("Teacher", uselist=False, back_populates="_class")

    students = relationship("Student", uselist=True, back_populates="_class")
    attendances = relationship("Attendance", uselist=True, back_populates="_class")
