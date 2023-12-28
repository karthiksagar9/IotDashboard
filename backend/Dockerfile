FROM python:latest

WORKDIR /backend
COPY pyproject.toml poetry.lock /backend/


RUN pip install poetry
RUN poetry install
COPY ./backend /backend
RUN poetry config virtualenvs.in-project true

#RUN poetry install

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]






