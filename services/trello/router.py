from fastapi import APIRouter, status

from api.setup import trello_service
from services.auth.handlers import UserDependsType
from services.trello.models import (
    TrelloAuthURLResponse,
    TrelloUserTokenSet,
    TrelloUserTokenSetResult,
)

router = APIRouter(tags=["trello"])


@router.get(
    path="/auth_url/",
    status_code=status.HTTP_200_OK,
    response_model=TrelloAuthURLResponse,
)
def get_auth_url(_: UserDependsType):
    """
    Returns the url needed to obtain access token from Trello
    """
    return TrelloAuthURLResponse(url=trello_service.authorization_url)


@router.post(
    path="/set_token/",
    status_code=status.HTTP_200_OK,
    response_model=TrelloUserTokenSetResult,
)
def user_token_set(user: UserDependsType, data: TrelloUserTokenSet):
    """
    Set relationshipt between local user and trello access token
    """
    return TrelloUserTokenSetResult(
        result=trello_service.set_user_trello_token(user_id=user.id, token=data.token)
    )
