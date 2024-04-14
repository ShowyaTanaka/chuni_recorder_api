FROM python:3.12-slim
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt upgrade -y && apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config gosu
RUN pip install --upgrade pip && pip install pipenv
COPY docker/app/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY Pipfile Pipfile.lock /app/
WORKDIR /app
RUN pipenv install --deploy --system
WORKDIR /
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
