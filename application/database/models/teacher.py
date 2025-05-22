from sqlalchemy.orm import relationship
from application.extensions import db
from application.database.models.person import Person

class Teacher(Person):
    __tablename__ = "Teacher"
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    _class = relationship("_Class", uselist=False, back_populates="teacher")
    grades = relationship("Grade", back_populates="teacher")
