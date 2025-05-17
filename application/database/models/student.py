from application.database.models.person import Person
from sqlalchemy import *
from sqlalchemy.orm import *

class Student(Person):
    __tablename__ = "Student"

    class_id = Column(Integer, ForeignKey("Class.id"), )
    _class = relationship("_Class", back_populates="students")

    attendances = relationship("Attendance", back_populates="student")

    grades = relationship("Grade", back_populates="student")
