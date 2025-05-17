from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()


class Person(Base):
    __abstract__ = True
    __allow__unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    pesel = Column(Integer, nullable=False)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)


class Teacher(Person):
    __tablename__ = "Teacher"
    _class = relationship("Class", uselist=False, back_populates="teacher")

    grades = relationship("Grade", back_populates="teacher")


class Student(Person):
    __tablename__ = "Student"

    class_id = Column(Integer, ForeignKey("Class.id"), )
    _class = relationship("Class", back_populates="students")

    attendances = relationship("Attendance", back_populates="student")

    grades = relationship("Grade", back_populates="student")


class Class(Base):
    __tablename__ = "Class"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    year = Column(Date, nullable=False)

    teacher_id = Column(Integer, ForeignKey("Teacher.id"))
    teacher = relationship("Teacher", uselist=False, back_populates="_class")

    students = relationship("Student", uselist=True, back_populates="_class")
    attendances = relationship("Attendance", uselist=True, back_populates="_class")


class Attendance(Base):
    __tablename__ = "Attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(30), nullable=False)
    date = Column(Date, nullable=False)

    class_id = Column(Integer, ForeignKey("Class.id"))
    _class = relationship("Class", uselist=False, back_populates="attendances")

    student_id = Column(Integer, ForeignKey("Student.id"))
    student = relationship("Student", uselist=False, back_populates="attendances")


class Grade(Base):
    __tablename__ = "Grade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=False)
    type = Column(String(30), nullable=False)

    student_id = Column(Integer, ForeignKey("Student.id"))
    student = relationship("Student", uselist=False, back_populates="grades")

    teacher_id = Column(Integer, ForeignKey("Teacher.id"))
    teacher = relationship("Teacher", uselist=False, back_populates="grades")
