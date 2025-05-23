from application.database.models import Grade, Student, _Class
from flask import session


def get_class_grade(db_session, class_id):
    res = []
    students = db_session.query(Student).filter(Student.class_id == class_id).all()
    for student in students:
        grades = Grade.query.filter_by(student_id=student.id).all()
        avg = round(sum(g.value for g in grades) / len(grades), 2) if grades else None
        res.append({
            "id": student.id,
            "student_name": student.name,
            "student_surname": student.surname,
            "grades": [g.value for g in grades],
            "avg": avg,
        })
    return res


def get_all_grades_students_classes(db_session):
    grades = db_session.query(Grade).join(Student).join(_Class).filter(_Class.teacher_id == session["teacher_id"]).all()

    students = {}

    for grade in grades:
        student = grade.student
        student_id = student.id

        if student_id not in students:
            students[student_id] = {
                "student_name": student.name,
                "student_surname": student.surname,
                "class_name": student._class.name,
                "class_id": student._class.id,
                "grades_list": [],
            }

        students[student_id]["grades_list"].append(grade.value)

    for student_data in students.values():
        grades_list = student_data["grades_list"]
        student_data["avg_grade"] = sum(grades_list) / len(grades_list) if grades_list else 0

    return list(students.values())
