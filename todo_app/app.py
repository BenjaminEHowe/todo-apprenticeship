import flask

from todo_app.config import FlaskConfig, TrelloConfig
from todo_app.trello import Trello

app = flask.Flask(__name__)
app.config.from_object(FlaskConfig)

trello = Trello(TrelloConfig.KEY, TrelloConfig.TOKEN, TrelloConfig.BOARD_ID) # pylint: disable=no-member

@app.route('/')
def index():
    lists = trello.get_lists()
    items = {}
    for lst in lists:
        items[lst['id']] = trello.get_items(lst['id'])
    return flask.render_template('index.html', lists = lists, items = items)


@app.route('/items', methods=['POST'])
def add_task():
    title = flask.escape(flask.request.form['title'])
    trello.add_item(title)
    return flask.render_template('item_created.html', item_title = title), 201


if __name__ == '__main__':
    app.run()
