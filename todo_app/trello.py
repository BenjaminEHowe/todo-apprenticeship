import requests


TRELLO_PREFIX = 'trello_'


class Trello:
    def __init__(self, key, token, boardId):
        self._key = key
        self._token = token
        self._boardId = boardId
        self._lists = []
        self._populate_board_with_lists()
        trelloLists = self._get_lists_on_board()
        for trelloList in trelloLists:
            lst = {}
            lst['id'] = TRELLO_PREFIX + trelloList['id']
            lst['name'] = trelloList['name']
            self._lists.append(lst)

    def add_item(self, title):
        toDoListId = next(lst['id'] for lst in self._lists if lst['name'] == 'To Do')
        self._create_card_on_list(toDoListId, title)
    
    def get_items(self):
        trelloItems = self._get_cards_on_board()
        items = []
        for trelloItem in trelloItems:
            item = {}
            item['id'] = TRELLO_PREFIX + trelloItem['id']
            item['list'] = next(lst['name'] for lst in self._lists if lst['id'] == TRELLO_PREFIX + trelloItem['idList'])
            item['title'] = trelloItem['name']
            items.append(item)
        return items

    def _create_card_on_list(self, listId, name):
        if listId.startswith(TRELLO_PREFIX):
            listId = listId[len(TRELLO_PREFIX):]
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

    def _get_cards_on_board(self):
        url = 'https://api.trello.com/1/boards/{}/cards'.format(self._boardId)
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
        expectedLists = ('To Do', 'In Progress', 'Done')
        for listName in expectedLists:
            if not next((lst for lst in lists if lst['name'] == listName), None):
                self._create_list(listName)

