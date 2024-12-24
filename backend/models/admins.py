from models import BaseModel
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admin(BaseModel):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)

    def set_password(self, password: str) -> None:
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<Admin {self.username}>"
