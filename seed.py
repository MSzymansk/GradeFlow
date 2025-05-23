# application/seed.py
from datetime import date, timedelta
import random
from werkzeug.security import generate_password_hash
from application.extensions import db
from application.database.models import Teacher, _Class, Student, Grade, Attendance

def seed_data():
    if Teacher.query.first():  # sprawdzamy czy dane już istnieją
        return


    teacher1 = Teacher(pesel=22222222222, name="Jan", surname="Nowak",email="jan@n.pl",password=generate_password_hash("jan"))
    teacher2 = Teacher(pesel=22222222222, name="Jan", surname="Waclaw",email="jan@w",password=generate_password_hash("jan"))
    teacher3 = Teacher(pesel=33333333333, name="Maria", surname="Wiśniewska",email="maria@w.pl",password=generate_password_hash("maria"))
    db.session.add_all([teacher1, teacher2, teacher3])
    db.session.flush()

    class1 = _Class(name="1A", year=date(2023, 9, 1), teacher=teacher1)
    class2 = _Class(name="2B", year=date(2023, 9, 1), teacher=teacher2)
    class3 = _Class(name="3C", year=date(2023, 9, 1), teacher=teacher3)
    db.session.add_all([class1, class2, class3])
    db.session.flush()

    students = [
        Student(pesel=44444444401, name="Adam", surname="Bąk", _class=class1),
        Student(pesel=44444444402, name="Ewa", surname="Lis", _class=class1),
        Student(pesel=44444444403, name="Kuba", surname="Mazur", _class=class1),
        Student(pesel=44444444404, name="Zofia", surname="Dąbrowska", _class=class2),
        Student(pesel=44444444405, name="Tomasz", surname="Wójcik", _class=class2),
        Student(pesel=44444444406, name="Natalia", surname="Kamińska", _class=class2),
        Student(pesel=44444444407, name="Michał", surname="Krawczyk", _class=class3),
        Student(pesel=44444444408, name="Oliwia", surname="Piotrowska", _class=class3),
        Student(pesel=44444444409, name="Patryk", surname="Grabowski", _class=class3),
        Student(pesel=44444444410, name="Laura", surname="Zielińska", _class=class3),
    ]
    db.session.add_all(students)
    db.session.flush()

    for student in students:
        teacher = student._class.teacher

        for _ in range(2):
            grade = Grade(
                value=random.choice([3, 4, 5, 6]),
                type=random.choice(["sprawdzian", "kartkówka", "odpowiedź"]),
                student=student,
                teacher=teacher
            )
            db.session.add(grade)

        for i in range(2):
            attendance = Attendance(
                status=random.choice(["obecny", "nieobecny", "spóźniony"]),
                date=date.today() - timedelta(days=i),
                _class=student._class,
                student=student
            )
            db.session.add(attendance)

    db.session.commit()
