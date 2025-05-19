from application.extensions import db


class Grade(db.Model):
    __tablename__ = "Grade"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(30), nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey("Student.id"))
    student = db.relationship("Student", uselist=False, back_populates="grades")

    teacher_id = db.Column(db.Integer, db.ForeignKey("Teacher.id"))
    teacher = db.relationship("Teacher", uselist=False, back_populates="grades")