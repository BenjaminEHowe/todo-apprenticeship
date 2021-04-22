import flask
from flask.globals import session
import todo_app.data.session_items as session_items

from todo_app.flask_config import Config

app = flask.Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return flask.render_template('index.html', tasks = session_items.get_items())


@app.route('/items', methods=['POST'])
def add_task():
    title = flask.escape(flask.request.form['title'])
    session_items.add_item(title)
    return flask.render_template('item_created.html', item_title = title), 201


if __name__ == '__main__':
    app.run()
