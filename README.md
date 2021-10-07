# DevOps Apprenticeship: Project Exercise

The project can be run using [Vagrant](https://www.vagrantup.com/) or natively.

Regardless, you'll need to create a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). A few variables will need to be set as part of the first setup:
- [`SECRET_KEY`](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY): used to encrypt the flask session cookie.
- `TRELLO_KEY` and `TRELLO_TOKEN`: Trello API credentials which can be obtained from the [Trello Developer API keys page](https://trello.com/app-key).
- `TRELLO_BOARD_ID`: the ID of the Trello board to use for the tasks.

## Using Vagrant

Install the latest versions of [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/), and then run `vagrant up` in the project directory. The initial set-up process will take a few minutes, and then the application will run on [`http://localhost:5000/`](http://localhost:5000/).

## Native installation

### System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

#### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

#### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

### Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

### Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

To run the unit and integrations tests, run `poetry run pytest tests`.

To run the end to end tests:
- [Install Firefox](https://www.mozilla.org/en-GB/firefox/new/)
- Download [geckodriver](https://github.com/mozilla/geckodriver/releases) (selecting the correct build for your OS / CPU architecture) and place it in the "bin" directory with the name "geckodriver"
- Run `poetry run pytest tests_e2e`

(note that the end to end tests requre valid `TRELLO_KEY` and `TRELLO_TOKEN` values to be set in the `.env` file, althought the value of `TRELLO_BOARD_ID` is ignored)
