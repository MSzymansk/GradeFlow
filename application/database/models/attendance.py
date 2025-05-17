from sqlalchemy import *
from sqlalchemy.orm import *
from application.database.models import Base


class Attendance(Base):
    __tablename__ = "Attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(30), nullable=False)
    date = Column(Date, nullable=False)

    class_id = Column(Integer, ForeignKey("Class.id"))
    _class = relationship("_Class", uselist=False, back_populates="attendances")

    student_id = Column(Integer, ForeignKey("Student.id"))
    student = relationship("Student", uselist=False, back_populates="attendances")
