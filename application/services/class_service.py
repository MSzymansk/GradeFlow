from application.database.models import _Class, Student
from sqlalchemy import *
from flask import session


def get_all_classes_from_db(db_session):
    classes = db_session.query(_Class).filter(_Class.teacher_id == session["teacher_id"]).all()
    return [
        {
            "id": _class.id,
            "name": _class.name
        }
        for _class in classes
    ]
