# from typing import Annotated
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    APIKeyQuery,
    OAuth2PasswordBearer,
    HTTPBearer,
)
from starlette.authentication import AuthenticationBackend
from jose import jwt, JWTError
from starlette.requests import Request

# from db import get_db
from utils import get_admin_by_username, get_auth_admin
# from models import Admin
from config import *

from schemas import TokenData


AUTH_KEY = os.environ.get("APPLICATION_API_KEY", "1")
AUTH_KEY_NAME = "access_token"

auth_key_query = APIKeyQuery(name=AUTH_KEY_NAME, auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_security = HTTPBearer()
basic_security = HTTPBasic()


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        authorization = request.headers.get("Authorization")
        try:
            scheme, token = authorization.split()
        except (ValueError, AttributeError):
            return False, None
        if scheme.lower() != "bearer":
            return False, None
        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_KEY,
                algorithms=[ALGORITHM],
                options={
                    "verify_exp": False,
                },
            )
            username: str = payload.get("sub")
            admin = await get_admin_by_username(username=username)
        except JWTError:
            return False, None
        if admin:
            return True, admin
        return False, None


def get_basic_credentials(
    credentials: HTTPBasicCredentials = Depends(basic_security),
) -> tuple[str, str]:
    username, password = credentials.username, credentials.password
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
        )
    return username, password


# async def get_current_admin(credentials: tuple = Security(get_basic_credentials)) -> Admin:
#     username, password = credentials
#         admin = await get_auth_admin(username=username, password=password)
#     if not admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid authentication credentials",
#         )
#     return admin


# async def validate_auth(token: Annotated[str, Depends(bearer_security)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     return token_data
#
#
# async def get_current_master_user(
#     token: Annotated[TokenData, Depends(validate_auth)], db=Depends(get_db)
# ):
#     master_user = await get_master_user_by_username(username=token.username, db=db)
#     if not master_user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid authentication credentials",
#         )
#     return master_user
