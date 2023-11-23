import uuid

import httpx
from fastapi import HTTPException, status

from api.config import (
    TRELLO_API_KEY,
    TRELLO_TOKEN_EXPIRATION,
    TRELLO_TOKEN_NAME,
    TRELLO_TOKEN_USER_DATA_KEY,
)
from services.users.models import UsersQuery, UserUpdateModel
from services.users.service import UsersService


class TrelloService:
    """
    A service class for retrieving and formatting weather data.
    """

    BASE_URL = "https://api.trello.com/1"

    def __init__(self, users_service: UsersService) -> None:
        self.users_service = users_service

    @property
    def authorization_url(self) -> str:
        base_url = "https://trello.com/1/authorize"
        scope = "read,write"
        return f"{base_url}?expiration={TRELLO_TOKEN_EXPIRATION}&name={TRELLO_TOKEN_NAME}&scope={scope}&response_type=token&key={TRELLO_API_KEY}"

    def set_user_trello_token(self, user_id: uuid.UUID, token: str) -> bool:
        query = UsersQuery(id=user_id)
        key = TRELLO_TOKEN_USER_DATA_KEY
        data = UserUpdateModel(external_data={key: token})
        updated = self.users_service.update(query=query, data=data)
        return bool(updated)

    def _request(
        self,
        token: str,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
    ):
        url = f"{self.BASE_URL}{endpoint}"

        params = (params or {}) | {"key": TRELLO_API_KEY, "token": token}

        if method == "GET":
            response = httpx.get(url, params=params)
        elif method == "POST":
            response = httpx.post(url, params=params, json=data)
        else:
            raise ValueError(f"Invalid method: {method}")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Error conecting to Trello API, have a valid token asociated with your user?",
            )
        return response.json()

    @staticmethod
    def _filter_data(entry: dict, data: dict) -> bool:
        data = {k: v for k, v in data.items() if v}
        for key, value in data.items():
            if entry.get(key) != value:
                return False
        return True

    def query_boards(
        self,
        token: str,
        id: str = None,
        name: str = None,
    ) -> list[dict]:
        endpoint = "/members/me/boards/"
        boards = self._request(token=token, method="GET", endpoint=endpoint)
        filter_data = dict(id=id, name=name)
        return list(filter(lambda x: self._filter_data(x, data=filter_data), boards))

    def query_lists(
        self,
        token: str,
        board_id: str,
        id: str = None,
        name: str = None,
    ) -> list[dict]:
        endpoint = f"/boards/{board_id}/lists/"
        trello_lists = self._request(token=token, method="GET", endpoint=endpoint)
        filter_data = dict(id=id, name=name)
        return list(
            filter(lambda x: self._filter_data(x, data=filter_data), trello_lists)
        )

    def query_labels(self, token: str, board_id: str, id: str = None, name: str = None):
        endpoint = f"/boards/{board_id}/labels"

        labels = self._request(token=token, method="GET", endpoint=endpoint)
        filter_data = dict(id=id, name=name)

        return list(
            filter(lambda x: self._filter_data(entry=x, data=filter_data), labels)
        )

    def create_board(self, token: str, name: str):
        endpoint = "/boards/"
        params = {"name": name}

        return self._request(
            token=token, method="POST", endpoint=endpoint, params=params
        )

    def get_or_create_board(self, token: str, name: str) -> dict:
        board = next(
            iter(self.query_boards(token=token, name=name)),
            None,
        )
        if board is None:
            board = self.create_board(token=token, name=name)
        return board

    def get_board_members(self, token: str, board_id: str):
        endpoint = f"/boards/{board_id}/members"
        return self._request(token=token, method="GET", endpoint=endpoint)

    def create_list(self, token: str, board_id: str, name: str) -> list[dict]:
        endpoint = "/lists"
        params = {"name": name, "idBoard": board_id}
        return self._request(
            token=token, method="POST", endpoint=endpoint, params=params
        )

    def get_or_create_list(self, token: str, board_id: str, name: str) -> dict:
        trello_list = next(
            iter(self.query_lists(token=token, board_id=board_id, name=name))
        )
        if trello_list is None:
            trello_list = self.create_list(token=token, board_id=board_id, name=name)
        return trello_list

    def create_label(
        self, token: str, board_id: str, color: str = None, name: str = None
    ) -> dict:
        endpoint = f"/labels/"
        params = {"idBoard": board_id, "color": color, "name": name}
        return self._request(
            token=token, method="POST", endpoint=endpoint, params=params
        )

    def get_or_create_label(self, token: str, board_id: str, name: str) -> dict:
        label = next(
            iter(self.query_labels(token=token, board_id=board_id, name=name)),
            None,
        )
        if label is None:
            label = self.create_label(token=token, board_id=board_id, name=name)
        return label

    def create_card(
        self,
        token: str,
        list_id: str,
        name: str,
        description=None,
        labels: list[str] = None,
        members: list[str] = None,
    ) -> dict:
        endpoint = "/cards/"
        params = {
            "idList": list_id,
            "name": name,
            "idLabels": labels or [],
            "idMembers": members or [],
        }
        if description:
            params["desc"] = description
        return self._request(
            token=token, method="POST", endpoint=endpoint, params=params
        )
