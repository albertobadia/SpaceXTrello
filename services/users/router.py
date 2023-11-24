from fastapi import APIRouter, HTTPException, status

from api.setup import users_service
from services.auth.handlers import UserDependsType
from services.auth.models import Token
from services.auth.service import AuthService
from services.users.models import UserCreate, UserRead

router = APIRouter(tags=["users"])


@router.post(
    path="/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
def create_user(user: UserCreate):
    """
    Creates a new user with the given user data.

    Args:
        user (UserCreate): The user data to create the new user with.

    Returns:
        UserRead: The newly created user.
    """
    try:
        user = users_service.create(user=user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        ) from e
    return UserRead(**user.model_dump())


@router.post(
    path="/login/",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
def login(data: UserCreate) -> Token:
    """
    Authenticates a user and returns an access token.

    Args:
        data (UserCreate): The user's login credentials.

    Returns:
        Token: An access token for the authenticated user.
    """
    user = users_service.authenticate(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AuthService.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)


@router.get("/me/", response_model=UserRead)
def me(current_user: UserDependsType):
    """
    Returns the current user.

    Args:
        current_user (UserDependsType): The current user.

    Returns:
        UserDependsType: The current user.
    """
    return current_user
