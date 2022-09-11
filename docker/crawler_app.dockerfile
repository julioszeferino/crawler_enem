FROM python:3.10.7-slim
LABEL maintainer "Julio Zeferino <julioszeferino@gmail.com>"
COPY . /var/www/crawler
WORKDIR /var/www/crawler
RUN pip install -r requirements.txt
ENTRYPOINT alembic upgrade head && python run.py