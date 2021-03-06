def create_app():
    import flask

    from todo_app.config.flask import FlaskConfig
    from todo_app.config.trello import TrelloConfig
    from todo_app.models import ViewModel
    from todo_app.trello import Trello
    
    app = flask.Flask(__name__)
    app.config.from_object(FlaskConfig)
    trello = Trello(TrelloConfig)
    

    @app.route('/')
    def index():
        return flask.render_template('index.html', model=ViewModel(lists=trello.get_lists_with_cards()))


    @app.route('/items/<id>/edit', methods=['GET'])
    def edit_item_page(id):
        return flask.render_template('item_edit.html', item = trello.get_item(id), lists = trello.get_lists())


    @app.route('/items', methods=['POST'])
    def add_item():
        title = flask.escape(flask.request.form['title'])
        trello.add_item(title)
        return flask.render_template('item_created.html', item_title = title), 201


    @app.route('/items/<id>', methods=['PATCH'])
    def update_item(id):
        trello.update_item(id, flask.request.json)
        return '', 204
    
    return app


if __name__ == '__main__':
    create_app().run()
