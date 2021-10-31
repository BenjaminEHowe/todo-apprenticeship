FROM python:3.8.4-buster as base
ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
EXPOSE 5000
WORKDIR /todo-apprenticeship
COPY . /todo-apprenticeship/

FROM base as development
RUN poetry config virtualenvs.create false --local
RUN poetry install
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000

FROM base as production
ENV FLASK_ENV=production
RUN poetry config virtualenvs.create false --local
RUN poetry install
RUN poetry add gunicorn
ENTRYPOINT poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:5000
