import pytest

import todo_app.constants as constants
from todo_app.models import ViewModel
from todo_app.trello import TrelloCard, TrelloListWithCards

def test_viewmodel_todo_list():
    """Test that the ViewModel returns the items from the "To Do" list."""
    TEST_CARD_ID = 'id_card'
    LIST_ID = 'id_todo'
    viewModel = ViewModel(lists=(TrelloListWithCards(LIST_ID, constants.LIST_NAME_TODO, (TrelloCard(TEST_CARD_ID, LIST_ID, 'title'), )), ))
    assert len(viewModel.todo_list.items) == 1
    assert viewModel.todo_list.items[0].id == TEST_CARD_ID

def test_viewmodel_inprogress_list():
    """Test that the ViewModel returns the items from the "In Progress" list."""
    TEST_CARD_ID = 'id_card'
    LIST_ID = 'id_inprogress'
    viewModel = ViewModel(lists=(TrelloListWithCards(LIST_ID, constants.LIST_NAME_INPROGRESS, (TrelloCard(TEST_CARD_ID, LIST_ID, 'title'), )), ))
    assert len(viewModel.inprogress_list.items) == 1
    assert viewModel.inprogress_list.items[0].id == TEST_CARD_ID

def test_viewmodel_done_list():
    """Test that the ViewModel returns the items from the "Done" list."""
    TEST_CARD_ID = 'id_card'
    LIST_ID = 'id_done'
    viewModel = ViewModel(lists=(TrelloListWithCards(LIST_ID, constants.LIST_NAME_DONE, (TrelloCard(TEST_CARD_ID, LIST_ID, 'title'), )), ))
    assert len(viewModel.done_list.items) == 1
    assert viewModel.done_list.items[0].id == TEST_CARD_ID
