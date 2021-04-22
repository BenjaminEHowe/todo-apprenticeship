import flask
from flask.globals import session
import todo_app.data.session_items as session_items

from todo_app.flask_config import Config

app = flask.Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return flask.render_template('index.html', tasks = session_items.get_items())


if __name__ == '__main__':
    app.run()
