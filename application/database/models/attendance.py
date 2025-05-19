from application.extensions import db



class Attendance(db.Model):
    __tablename__ = "Attendance"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=False)

    class_id = db.Column(db.Integer, db.ForeignKey("Class.id"))
    _class = db.relationship("_Class", uselist=False, back_populates="attendances")

    student_id = db.Column(db.Integer, db.ForeignKey("Student.id"))
    student = db.relationship("Student", uselist=False, back_populates="attendances")
