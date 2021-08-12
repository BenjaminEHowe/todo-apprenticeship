from typing import Tuple
import requests
from dataclasses import dataclass

import todo_app.constants as constants


TRELLO_PREFIX = 'trello_'


def remove_trello_prefix_if_exists(id):
        if id.startswith(TRELLO_PREFIX):
            id = id[len(TRELLO_PREFIX):]
        return id


class Trello:
    def __init__(self, config):
        self._key = config.KEY
        self._token = config.TOKEN
        self._boardId = config.BOARD_ID
        self._populate_board_with_lists()

    def add_item(self, title):
        toDoListId = next(lst.id for lst in self.get_lists() if lst.name == constants.LIST_NAME_TODO)
        self._create_card_on_list(toDoListId, title)

    def get_item(self, itemId):
        itemId = remove_trello_prefix_if_exists(itemId)
        return TrelloCard.from_trello(self._get_card(itemId))
    
    def get_items(self, listId):
        trelloCards = self._get_cards_in_list(listId)
        items = []
        for card in trelloCards:
            items.append(TrelloCard.from_trello(card))
        return tuple(items)
    
    def get_lists(self):
        lists = []
        trelloLists = self._get_lists_on_board()
        for trelloList in trelloLists:
            lists.append(TrelloList.from_trello(trelloList))
        return tuple(lists)

    def get_lists_with_cards(self):
        lists = self.get_lists()
        cards = []
        for card in self._get_cards_on_board():
            cards.append(TrelloCard.from_trello(card))
        listsWithCards = []
        for list_ in lists:
            listsWithCards.append(list_.add_cards(tuple([card for card in cards if card.listId == list_.id])))
        return tuple(listsWithCards)
    
    def update_item(self, itemId, updatedFields):
        itemId = remove_trello_prefix_if_exists(itemId)
        for field in updatedFields:
            if field not in ('title', 'listId'):
                raise ValueError(f'{field} cannot be updated!')
        trelloUpdatedFields = {}
        if 'title' in updatedFields:
            trelloUpdatedFields['name'] = updatedFields['title']
        if 'listId' in updatedFields:
            trelloUpdatedFields['idList'] = remove_trello_prefix_if_exists(updatedFields['listId'])
        self._update_card(itemId, trelloUpdatedFields)

    def _create_card_on_list(self, listId, name):
        listId = remove_trello_prefix_if_exists(listId)
        url = 'https://api.trello.com/1/cards'
        query = {
            'key': self._key,
            'token': self._token,
            'idList': listId,
            'name': name,
            'pos': 'bottom'
        }
        r = requests.post(url, params=query)
        return r.json()


    def _create_list(self, listName):
        url = 'https://api.trello.com/1/boards/{}/lists'.format(self._boardId)
        query = {
            'key': self._key,
            'token': self._token,
            'name': listName,
            'pos': 'bottom'
        }
        r = requests.post(url, params=query)
        return r.json()
    
    def _get_card(self, cardId):
        url = 'https://api.trello.com/1/cards/{}'.format(cardId)
        query = { 'key': self._key, 'token': self._token }
        r = requests.get(url, params=query)
        return r.json()

    def _get_cards_on_board(self):
        url = 'https://api.trello.com/1/boards/{}/cards'.format(self._boardId)
        query = { 'key': self._key, 'token': self._token }
        r = requests.get(url, params=query)
        return r.json()

    def _get_cards_in_list(self, listId):
        listId = remove_trello_prefix_if_exists(listId)
        url = 'https://api.trello.com/1/lists/{}/cards'.format(listId)
        query = { 'key': self._key, 'token': self._token }
        r = requests.get(url, params=query)
        return r.json()

    def _get_lists_on_board(self):
        url = 'https://api.trello.com/1/boards/{}/lists'.format(self._boardId)
        query = { 'key': self._key, 'token': self._token }
        r = requests.get(url, params=query)
        return r.json()

    def _populate_board_with_lists(self):
        lists = self._get_lists_on_board()
        expectedLists = (constants.LIST_NAME_TODO, constants.LIST_NAME_INPROGRESS, constants.LIST_NAME_DONE)
        for listName in expectedLists:
            if not next((lst for lst in lists if lst['name'] == listName), None):
                self._create_list(listName)
    
    def _update_card(self, cardId, trelloUpdatedFields):
        url = f'https://api.trello.com/1/cards/{cardId}'
        query = { 'key': self._key, 'token': self._token }
        r = requests.put(url, params={**query, **trelloUpdatedFields})
        return r.json()


@dataclass(frozen=True)
class TrelloCard:
    id: str
    listId: str
    title: str
    
    @classmethod
    def from_trello(cls, trelloData):
        return cls(trelloData['id'], trelloData['idList'], trelloData['name'])


@dataclass(frozen=True)
class TrelloList:
    id: str
    name: str
    
    @classmethod
    def from_trello(cls, trelloData):
        return cls(trelloData['id'], trelloData['name'])
    
    def add_cards(self, cards: tuple):
        return TrelloListWithCards(self.id, self.name, cards)
    

@dataclass(frozen=True)
class TrelloListWithCards(TrelloList):
    items: Tuple[TrelloCard, ...]
