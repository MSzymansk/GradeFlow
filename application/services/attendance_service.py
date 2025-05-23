from collections import defaultdict
from flask import session
from application.database.models import Attendance, _Class, student, Student, teacher
from sqlalchemy.orm import selectinload


def get_attendance_summary_by_teacher(db_session):
    classes = db_session.query(_Class) \
        .options(
        selectinload(_Class.students).selectinload(Student.attendances)
    ) \
        .filter(_Class.teacher_id == session["teacher_id"]) \
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


def get_lessons(db_session):
    lessons = db_session.query(Attendance)\
        .join(_Class, Attendance.class_id == _Class.id)\
        .options(selectinload(Attendance.student), selectinload(Attendance._class))\
        .filter(_Class.teacher_id == session["teacher_id"])\
        .all()

    grouped = defaultdict(list)

    for lesson in lessons:
        key = (lesson.date, lesson._class.name)
        grouped[key].append({
            "imie": lesson.student.name,
            "nazwisko": lesson.student.surname,
            "status": lesson.status
        })

    result = []
    for (date, class_name), students in grouped.items():
        result.append({
            "data": date.isoformat(),
            "klasa": class_name,
            "uczniowie": students
        })

    return result

def get_lessons_list(db_session):
    lessons = db_session.query(Attendance)\
        .join(_Class, Attendance.class_id == _Class.id)\
        .filter(_Class.teacher_id == session["teacher_id"]).all()

    result_set = set()

    for lesson in lessons:
        result_set.add((lesson.date.isoformat(), lesson._class.name))


    result = [
        {"data": date, "klasa": class_name}
        for (date, class_name) in sorted(result_set)
    ]

    return result

