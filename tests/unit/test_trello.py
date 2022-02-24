import os
import unittest.mock

import todo_app.constants as constants
from todo_app.trello import Trello

class TrelloConfig:
    KEY = 'invalid'
    TOKEN = 'invalid'
    BOARD_ID = 'test_board_id'

def mock_trello_requests(url, params):
    TEST_BOARD_ID = os.getenv('TRELLO_BOARD_ID')
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = unittest.mock.Mock()
        response.json.return_value = [
            {
                'id': '1',
                'name': constants.LIST_NAME_TODO,
            },
            {
                'id': '2',
                'name': constants.LIST_NAME_INPROGRESS
            },
            {
                'id': '3',
                'name': constants.LIST_NAME_DONE
            },
        ]
        return response
    return None

@unittest.mock.patch('requests.get')
def test_trello_expected_lists(mock_requests_get):
    """Test that the trello class creates and retrieves (at least) the expected lists."""
    mock_requests_get.side_effect = mock_trello_requests
    expectedLists = (constants.LIST_NAME_TODO, constants.LIST_NAME_INPROGRESS, constants.LIST_NAME_DONE)
    trello = Trello(TrelloConfig)
    trelloListNames = (list.name for list in trello.get_lists())
    for list in expectedLists:
        assert list in trelloListNames
