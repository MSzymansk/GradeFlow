from application.database.models import Grade, Student, _Class


def get_class_grade(session, class_id):
    res = []
    students = session.query(Student).filter(Student.class_id == class_id).all()
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


def get_all_grades_students_classes(session):
    grades = session.query(Grade).join(Student).join(_Class).all()
    print(grades)
    return [{
        "id": grade.id,
        "value": grade.value,
        "type": grade.type,
        "student_name": grade.student.name,
        "student_surname": grade.student.surname,
        "class_name": grade.student._class.name,
        "class_id" : grade.student._class.id
    }
        for grade in grades
    ]