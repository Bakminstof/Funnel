FROM python:3.11
LABEL authors="adnrey"

USER root

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip "poetry==1.7.1"
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev

COPY docker_init.sh .
RUN chmod 755 /docker_init.sh

COPY alembic.ini .
COPY alembic alembic
COPY src ./src

ENTRYPOINT ["/docker_init.sh"]

CMD ["python", "/src/main.py"]
