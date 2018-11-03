FROM python:3.6-alpine
WORKDIR /usr/src/app/web

RUN apk update && apk add postgresql-dev gcc musl-dev nginx supervisor

ADD requirements.txt .
RUN pip install -r requirements.txt

# RUN THE BELOW WHEN YOU NEED TO RUN THE DJANGO DB SHELL
#RUN apt-get install -y wget &&  wget -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add - && echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list && apt-get update && apt-get install -y postgresql-client-9.6

COPY start.sh .
COPY nginx.conf /etc/nginx/
COPY supervisor.conf /

COPY web .
CMD ./start.sh
