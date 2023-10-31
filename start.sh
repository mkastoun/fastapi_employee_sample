#!/bin/bash

pip install poetry
# install packages in case something missing
#poetry install

# Apply database migrations
poetry run alembic upgrade head

# run tests
poetry run pytest

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000
