from application.database.models import _Class, Student
from sqlalchemy import *


def get_all_classes_from_db(session):
    classes = session.query(_Class).all()
    return [
        {
            "id": _class.id,
            "name": _class.name
        }
        for _class in classes
    ]
