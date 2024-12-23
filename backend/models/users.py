from models import BaseModel

from sqlalchemy import Column, Integer, String


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, unique=True)
    password = Column(String)

    def __str__(self):
        return self.username
    