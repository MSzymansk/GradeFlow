from sqlalchemy import *
from sqlalchemy.orm import *
from application.database.models import Base


class Person(Base):
    __abstract__ = True
    __allow__unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    pesel = Column(Integer, nullable=False)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
