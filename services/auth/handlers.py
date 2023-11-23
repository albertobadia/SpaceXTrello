import typing

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.config import ALGORITHM, SECRET_KEY
from api.setup import users_service
from services.users.models import UserRead, UsersQuery

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(token: typing.Annotated[str, Depends(oauth2_scheme)]):
    """
    Returns the user associated with the provided token.

    Args:
        token (str): The token to be validated.

    Raises:
        HTTPException: If the credentials could not be validated.

    Returns:
        User: The user associated with the provided token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_service.get(query=UsersQuery(username=username))
    if user is None:
        raise credentials_exception
    return user


UserDependsType = typing.Annotated[UserRead, Depends(get_current_user)]
