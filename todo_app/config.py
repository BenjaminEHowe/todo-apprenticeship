import os


class FlaskConfig:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")


class TrelloConfig():
    """Configuration for Trello integration."""
    pass


trelloVars = ('KEY', 'TOKEN', 'BOARD_ID')
for var in trelloVars:
    setattr(TrelloConfig, var, os.environ.get('TRELLO_{}'.format(var)))
    if not getattr(TrelloConfig, var):
        raise ValueError('No TRELLO_{} set. Did you follow the setup instructions?'.format(var))
