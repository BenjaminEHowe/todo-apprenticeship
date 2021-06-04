import requests


TRELLO_PREFIX = 'trello_'


def remove_trello_prefix_if_exists(id):
        if id.startswith(TRELLO_PREFIX):
            id = id[len(TRELLO_PREFIX):]
        return id


class Trello:
    def __init__(self, key, token, boardId):
        self._key = key
        self._token = token
        self._boardId = boardId
        self._lists = []
        self._populate_board_with_lists()
        trelloLists = self._get_lists_on_board()
        for trelloList in trelloLists:
            self._lists.append(TrelloList.from_trello(self, trelloList))

    def add_item(self, title):
        toDoListId = next(lst.id for lst in self._lists if lst.name == 'To Do')
        self._create_card_on_list(toDoListId, title)

    def get_item(self, itemId):
        itemId = remove_trello_prefix_if_exists(itemId)
        return TrelloCard.from_trello(self._get_card(itemId))

    
    def get_items(self, listId):
        trelloCards = self._get_cards_in_list(listId)
        items = []
        for card in trelloCards:
            items.append(TrelloCard.from_trello(card))
        return items

    
    def get_lists(self):
        return self._lists
    
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
        print(trelloUpdatedFields)
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
        expectedLists = ('To Do', 'In Progress', 'Done')
        for listName in expectedLists:
            if not next((lst for lst in lists if lst['name'] == listName), None):
                self._create_list(listName)
    
    def _update_card(self, cardId, trelloUpdatedFields):
        url = f'https://api.trello.com/1/cards/{cardId}'
        print(url)
        query = { 'key': self._key, 'token': self._token }
        print({**query, **trelloUpdatedFields})
        r = requests.put(url, params={**query, **trelloUpdatedFields})
        return r.json()


class TrelloCard:
    @property
    def id(self):
        return self._id

    @property
    def listId(self):
        return self._listId

    @property
    def title(self):
        return self._title
    
    def __init__(self, id, listId, title):
        self._id = TRELLO_PREFIX + id
        self._listId = TRELLO_PREFIX + listId
        self._title = title
    
    @staticmethod
    def from_trello(trelloData):
        return TrelloCard(trelloData['id'], trelloData['idList'], trelloData['name'])
    
    def __repr__(self):
        return f'TrelloCard({self.id}, {self.listId}, {self.title})'


class TrelloList:
    @property
    def id(self):
        return self._id

    @property
    def items(self):
        return self._trello.get_items(self.id)
    
    @property
    def name(self):
        return self._name
    
    def __init__(self, trello, id, name):
        self._trello = trello
        self._id = TRELLO_PREFIX + id
        self._name = name

    @staticmethod
    def from_trello(trello, trelloData):
        return TrelloList(trello, trelloData['id'], trelloData['name'])
    
    def __repr__(self):
        return f'TrelloList({self.id}, {self.name}, {self.items})'
