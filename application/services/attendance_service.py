from flask import session
from sqlalchemy.orm import selectinload

from application.database.models import Attendance, _Class, student, Student, teacher
from sqlalchemy.orm import selectinload


def get_attendance_summary_by_teacher(db_session):
    classes = db_session.query(_Class)\
        .options(
            selectinload(_Class.students).selectinload(Student.attendances)
        )\
        .filter(_Class.teacher_id == session["teacher_id"])\
        .all()

    result = []

    for clas in classes:
        class_data = {
            "classId": clas.id,
            "className": clas.name,
            "students": []
        }

        for student in clas.students:
            attendances = student.attendances
            class_attendances = [a for a in attendances if a.class_id == clas.id]

            present_count = sum(1 for a in class_attendances if a.status == "Present")
            absent_count = sum(1 for a in class_attendances if a.status == "Absent")
            late_count = sum(1 for a in class_attendances if a.status == "Late")

            class_data["students"].append({
                "studentId": student.id,
                "studentName": student.name,
                "studentSurname": student.surname,
                "present": present_count,
                "absent": absent_count,
                "late": late_count
            })

        result.append(class_data)

    return result



