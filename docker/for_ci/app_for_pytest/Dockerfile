FROM python:3.12-slim
ENV APP_PATH=/app
ENV DEBIAN_FRONTEND noninteractive
WORKDIR $APP_PATH
COPY Pipfile Pipfile.lock chuniscore_recorder/ config/ tests/ __init__.py manage.py pytest.ini $APP_PATH
RUN apt update && apt upgrade -y && apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config gosu
RUN pip install pipenv
RUN pipenv install --dev --system
