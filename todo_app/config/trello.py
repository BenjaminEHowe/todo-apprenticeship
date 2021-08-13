import os


class TrelloConfig:
    """Configuration for Trello integration."""
    pass


trelloVars = ('KEY', 'TOKEN', 'BOARD_ID')
for var in trelloVars:
    setattr(TrelloConfig, var, os.environ.get('TRELLO_{}'.format(var)))
    if not getattr(TrelloConfig, var):
        raise ValueError('No TRELLO_{} set. Did you follow the setup instructions?'.format(var))
