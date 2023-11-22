FROM python:3.8.10

ARG APP_NAME=my-arithmetic-tpuser
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.8
ARG POETRY_VERSION=1.7.1
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get upgrade -y

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN pip3 install tox

ENV PATH="$POETRY_HOME/bin:$PATH"


WORKDIR $APP_PATH
COPY ./poetry.lock ./pyproject.toml ./README.md ./

RUN poetry install

CMD ["bash"]