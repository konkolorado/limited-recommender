FROM python:3.6-alpine
WORKDIR /usr/src/app/web

RUN apk update && apk add postgresql-dev gcc musl-dev nginx supervisor

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY start.sh .
COPY nginx.conf /etc/nginx/
COPY supervisor.conf /

COPY web .
CMD ./start.sh
