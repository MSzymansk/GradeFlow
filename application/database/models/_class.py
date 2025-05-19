from application.extensions import db


class _Class(db.Model):
    __tablename__ = "Class"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Date, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey("Teacher.id"))
    teacher = db.relationship("Teacher", uselist=False, back_populates="_class")

    students = db.relationship("Student", back_populates="_class")
    attendances = db.relationship("Attendance", back_populates="_class")
