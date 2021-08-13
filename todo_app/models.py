from dataclasses import dataclass
from typing import Tuple

import todo_app.constants as constants
from todo_app.trello import TrelloList, TrelloListWithCards

@dataclass(frozen=True)
class ViewModel:
    lists: Tuple[TrelloListWithCards, ...]

    @property
    def todo_list(self):
        return next(list for list in self.lists if list.name == constants.LIST_NAME_TODO)

    @property
    def inprogress_list(self):
        return next(list for list in self.lists if list.name == constants.LIST_NAME_INPROGRESS)

    @property
    def done_list(self):
        return next(list for list in self.lists if list.name == constants.LIST_NAME_DONE)

