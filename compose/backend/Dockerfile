FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN python3 -m pip install tensorflow lungmask
RUN apt-get update
RUN apt-get install python3-opencv -y

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./backend/pyproject.toml ./backend/poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY ./backend /app
