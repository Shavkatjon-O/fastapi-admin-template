from typing import Union, Type
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from jwt import verify_password
from models import Admin


async def get_admin_by_username(
    username: str, db: Session = Depends(get_db)
) -> Union[Admin, None]:
    return db.query(Admin).filter(Admin.username == username).first()


async def authenticate_admin(
    username: str, password: str, db: Session = Depends(get_db)
) -> Union[Admin, bool]:
    admin = await get_admin_by_username(username, db=db)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin


async def get_auth_admin(
    username: str, password: str, db: Session = Depends(get_db)
) -> bool | Type[Admin]:
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return False
    if not admin.verify_password(password):
        return False
    return admin