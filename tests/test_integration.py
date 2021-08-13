import dotenv
import os
import pytest
import unittest.mock

import todo_app.app
import todo_app.constants as constants

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    test_app = todo_app.app.create_app()
    with test_app.test_client() as client:
        yield client

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
    elif url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/cards':
        response = unittest.mock.Mock()
        response.json.return_value = [
            {
                'id': 'card_1',
                'idList': '1',
                'name': 'To Do Card',
            },
            {
                'id': 'card_2',
                'idList': '2',
                'name': 'In Progress Card',
            },
            {
                'id': 'card_3',
                'idList': '3',
                'name': 'Done Card',
            },
        ]
        return response
    return None

@unittest.mock.patch('requests.get')
def test_index_page(mock_requests_get, client):
    mock_requests_get.side_effect = mock_trello_requests
    response = client.get('/')
    assert response.status_code == 200
    decoded_response = response.data.decode('utf-8')
    assert 'To Do Card' in decoded_response
    assert 'In Progress Card' in decoded_response
    assert 'Done Card' in decoded_response
