FROM python:3.12-slim
ENV APP_PATH=/app
ENV DEBIAN_FRONTEND noninteractive
WORKDIR $APP_PATH
COPY Pipfile Pipfile.lock chuniscore_recorder/ config/ tests/ __init__.py manage.py pytest.ini $APP_PATH
RUN pip install pipenv
RUN pipenv install --dev --system
