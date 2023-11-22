FROM python:3.8.10

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN pip3 install tox

ENV PATH="$HOME/.local/bin:$PATH"

COPY ./poetry.lock ./pyproject.toml ./README.md ./

RUN poetry install

RUN poetry lock --no-update

RUN apt-get update && apt-get upgrade -y

RUN pip install

CMD ["bash"]