from datetime import date, timedelta, time, datetime
import random
from werkzeug.security import generate_password_hash
from application.extensions import db
from application.database.models import Teacher, _Class, Student, Grade, Attendance


from datetime import date, timedelta, datetime
import random
from werkzeug.security import generate_password_hash
from application.extensions import db
from application.database.models import Teacher, _Class, Student, Grade, Attendance

def seed_data():
    if Teacher.query.first():
        return

    first_names = [
        "Adam", "Ewa", "Kuba", "Zofia", "Tomasz", "Natalia", "Michał",
        "Oliwia", "Patryk", "Laura", "Jan", "Anna", "Piotr", "Magdalena", "Mateusz"
    ]
    last_names = [
        "Nowak", "Kowalska", "Mazur", "Wiśniewska", "Wójcik", "Kamińska",
        "Krawczyk", "Piotrowska", "Grabowski", "Zielińska", "Duda", "Pawlak"
    ]


    teacher1 = Teacher(pesel=11111111111, name="Jan", surname="Nowak", email="jan@gradeflow.pl", password_hash=generate_password_hash("jan"))
    teacher2 = Teacher(pesel=22222222222, name="Anna", surname="Kowalska", email="anna@gradeflow.pl", password_hash=generate_password_hash("anna"))
    db.session.add_all([teacher1, teacher2])
    db.session.flush()


    classes = [
        _Class(name="1A", year=date(2023, 9, 1), teacher=teacher1),
        _Class(name="1B", year=date(2023, 9, 1), teacher=teacher1),
        _Class(name="2A", year=date(2023, 9, 1), teacher=teacher2),
        _Class(name="2B", year=date(2023, 9, 1), teacher=teacher2),
    ]
    db.session.add_all(classes)
    db.session.flush()

    students = []
    pesel_base = 44444444000
    student_count = 0

    for _class in classes:
        for i in range(10):
            student = Student(
                pesel=pesel_base + student_count + 1,
                name=random.choice(first_names),
                surname=random.choice(last_names),
                _class=_class
            )
            students.append(student)
            student_count += 1

    db.session.add_all(students)
    db.session.flush()

    for student in students:
        teacher = student._class.teacher

        for _ in range(4):
            grade = Grade(
                value=random.choice([2, 3, 4, 5, 6]),
                type=random.choice(["sprawdzian", "kartkówka", "odpowiedź"]),
                student=student,
                teacher=teacher
            )
            db.session.add(grade)

        for i in range(4):
            attendance = Attendance(
                status=random.choice(["obecny", "nieobecny", "spóźniony"]),
                date=date.today() - timedelta(days=i),
                time=datetime.now().time(),
                _class=student._class,
                student=student
            )
            db.session.add(attendance)

    db.session.commit()

