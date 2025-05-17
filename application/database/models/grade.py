from sqlalchemy import *
from sqlalchemy.orm import *
from application.database.models import Base

class Grade(Base):
    __tablename__ = "Grade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=False)
    type = Column(String(30), nullable=False)

    student_id = Column(Integer, ForeignKey("Student.id"))
    student = relationship("Student", uselist=False, back_populates="grades")

    teacher_id = Column(Integer, ForeignKey("Teacher.id"))
    teacher = relationship("Teacher", uselist=False, back_populates="grades")