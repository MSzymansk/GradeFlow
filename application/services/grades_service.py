from pyclbr import Class

from sqlalchemy.orm import selectinload

from application.database.models import Grade, Student, _Class


def get_class_grade(session,class_id):
    res = []
    students = session.query(Student).filter(Student.class_id == class_id).all()
    for student in students:
        grades = Grade.query.filter_by(student_id=student.id).all()
        avg = round(sum(g.value for g in grades) / len(grades), 2) if grades else None
        res.append({
            "id": student.id,
            "student_name": student.name,
            "student_surname": student.surname,
            "grades" : [g.value for g in grades],
            "avg": avg,
        })
    return res

def get_all_students_grades_by_class_request(session):
    classes = session.query(_Class).options(
        selectinload(_Class.students).selectinload(Student.grades)
    ).all()

    return [
        {
            "classId": c.id,
            "className": c.name,
            "students": [
                {
                    "studentId": s.id,
                    "studentName": s.name,
                    "studentSurname": s.surname,
                    "grades": [g.value for g in s.grades]
                }
                for s in c.students
            ]
        }
        for c in classes
    ]