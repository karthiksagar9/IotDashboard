Requirements

Docker >= 17.05
Python >= 3.7
Poetry


Poetry

Create the virtual environment and install dependencies with

poetry install

Spawn a shell inside the virtual environment with:
poetry shell

Start a development server locally:
poetry run uvicorn app.main:app --reload --host localhost --port 8000

Docker Compose

You can build and run the container with Docker Compose
docker compose build
docker compose up


For generating data:
Triggering the script from container, tried with celery to run as background task but faced some issue.

