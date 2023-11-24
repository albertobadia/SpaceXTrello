import json
import pathlib
from unittest.mock import patch

here = pathlib.Path(__file__).parent

create_board_fixture = json.loads(
    here.joinpath("fixtures/create_board.json").read_text()
)
create_card_fixture = json.loads(here.joinpath("fixtures/create_card.json").read_text())
create_label_fixture = json.loads(
    here.joinpath("fixtures/create_label.json").read_text()
)
get_boards_fixture = json.loads(here.joinpath("fixtures/get_boards.json").read_text())
get_labels_fixture = json.loads(here.joinpath("fixtures/get_labels.json").read_text())
get_lists_fixture = json.loads(here.joinpath("fixtures/get_lists.json").read_text())
get_members_fixture = json.loads(here.joinpath("fixtures/get_members.json").read_text())


class TrelloMockMixin:
    def start_mocks(self):
        self.mock_card_create()
        self.mock_create_board()
        self.mock_create_label()
        self.mock_get_board()
        self.mock_get_labels()
        self.mock_get_lists()
        self.mock_get_members()

    def mock_create_board(self):
        create_board_patch = patch("services.trello.service.TrelloService.create_board")
        self.create_board_mock = create_board_patch.start()
        self.addCleanup(create_board_patch.stop)
        self.create_board_mock.return_value = create_board_fixture

    def mock_card_create(self):
        card_create_patch = patch("services.trello.service.TrelloService.create_card")
        self.card_create_mock = card_create_patch.start()
        self.addCleanup(card_create_patch.stop)
        self.card_create_mock.return_value = create_card_fixture

    def mock_create_label(self):
        create_label_patch = patch("services.trello.service.TrelloService.create_label")
        self.create_label_mock = create_label_patch.start()
        self.addCleanup(create_label_patch.stop)
        self.create_label_mock.return_value = create_label_fixture

    def mock_get_board(self):
        get_boards_patch = patch("services.trello.service.TrelloService.query_boards")
        self.get_boards_mock = get_boards_patch.start()
        self.addCleanup(get_boards_patch.stop)
        self.get_boards_mock.return_value = get_boards_fixture

    def mock_get_labels(self):
        get_labels_patch = patch("services.trello.service.TrelloService.query_labels")
        self.get_labels_mock = get_labels_patch.start()
        self.addCleanup(get_labels_patch.stop)
        self.get_labels_mock.return_value = get_labels_fixture

    def mock_get_lists(self):
        get_lists_patch = patch("services.trello.service.TrelloService.query_lists")
        self.get_lists_mock = get_lists_patch.start()
        self.addCleanup(get_lists_patch.stop)
        self.get_lists_mock.return_value = get_lists_fixture

    def mock_get_members(self):
        get_members_patch = patch(
            "services.trello.service.TrelloService.get_board_members"
        )
        self.get_members_mock = get_members_patch.start()
        self.addCleanup(get_members_patch.stop)
        self.get_members_mock.return_value = get_members_fixture
