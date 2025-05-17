from sqlalchemy.orm import relationship

from application.database.models.person import Person

class Teacher(Person):
    __tablename__ = "Teacher"
    _class = relationship("_Class", uselist=False, back_populates="teacher")

    grades = relationship("Grade", back_populates="teacher")
