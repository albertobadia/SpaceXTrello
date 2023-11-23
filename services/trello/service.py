import httpx

from api.config import TRELLO_ACCESS_TOKEN, TRELLO_API_KEY


class TrelloService:
    """
    A service class for retrieving and formatting weather data.
    """

    BASE_URL = "https://api.trello.com/1"

    @property
    def authorization_url(self) -> str:
        base_url = "https://trello.com/1/authorize"
        expiration_days = 1
        token_name = "SpaceXTrelloAPI"
        scope = "read,write"
        return f"{base_url}={expiration_days}day&name={token_name}&scope={scope}&response_type=token&key={TRELLO_API_KEY}"

    def _request(self, method, endpoint, params=None, data=None):
        url = f"{self.BASE_URL}{endpoint}"

        params = (params or {}) | {"key": TRELLO_API_KEY, "token": TRELLO_ACCESS_TOKEN}

        if method == "GET":
            response = httpx.get(url, params=params)
        elif method == "POST":
            response = httpx.post(url, params=params, json=data)
        else:
            raise ValueError(f"Invalid method: {method}")

        response.raise_for_status()
        return response.json()

    @staticmethod
    def _filter_data(entry: dict, data: dict) -> bool:
        data = {k: v for k, v in data.items() if v}
        for key, value in data.items():
            if entry.get(key) != value:
                return False
        return True

    def query_boards(self) -> list[dict]:
        endpoint = "/members/me/boards/"
        return self._request(method="GET", endpoint=endpoint)

    def query_boards(
        self,
        id: str = None,
        name: str = None,
    ) -> list[dict]:
        endpoint = "/members/me/boards/"
        boards = self._request("GET", endpoint)
        filter_data = dict(id=id, name=name)
        return list(filter(lambda x: self._filter_data(x, data=filter_data), boards))

    def query_lists(
        self,
        board_id: str,
        id: str = None,
        name: str = None,
    ) -> list[dict]:
        endpoint = f"/boards/{board_id}/lists/"
        trello_lists = self._request("GET", endpoint)
        filter_data = dict(id=id, name=name)
        return list(
            filter(lambda x: self._filter_data(x, data=filter_data), trello_lists)
        )

    def query_labels(self, board_id: str, id: str = None, name: str = None):
        endpoint = f"/boards/{board_id}/labels"

        labels = self._request(method="GET", endpoint=endpoint)
        filter_data = dict(id=id, name=name)

        return list(
            filter(lambda x: self._filter_data(entry=x, data=filter_data), labels)
        )

    def create_board(self, name: str):
        endpoint = "/boards/"
        params = {"name": name}

        return self._request(method="POST", endpoint=endpoint, params=params)

    def create_label(self, board_id: str, color: str = None, name: str = None):
        endpoint = f"/labels/"
        params = {"idBoard": board_id, "color": color, "name": name}
        return self._request(method="POST", endpoint=endpoint, params=params)

    def create_card(
        self, board_id: str, name: str, desc=None, labels: list[str] = None
    ) -> dict:
        endpoint = "/cards/"

        trello_list = next(
            iter(self.query_lists(board_id=board_id, name="To Do")), None
        )
        if trello_list is None:
            raise ValueError("List not found")

        data = {"idList": trello_list["id"], "name": name, "idLabels": labels or []}
        if desc:
            data["desc"] = desc
        return self._request("POST", endpoint, data=data)

    def create_task(self, title: str = None, category: str = None) -> dict:
        board_name = "SPACE_X_BOARD"
        board = next(iter(self.query_boards(name=board_name)), None)
        if board is None:
            board = self.create_board(name=board_name)

        label = next(
            iter(self.query_labels(board_id=board["id"], name=category)),
            None,
        )
        if label is None:
            label = self.create_label(board_id=board["id"], name=category)

        return self.create_card(board_id=board["id"], name=title, labels=[label["id"]])
