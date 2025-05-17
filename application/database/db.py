from instan.config import DATABASE_URI
from application.database.models import Base
from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine(f'sqlite:///{DATABASE_URI}', echo=True)
Session = sessionmaker(bind=engine)

def init_database():
    Base.metadata.create_all(engine)

def get_session():
    return Session()