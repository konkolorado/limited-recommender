#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE TABLE books(
    ISBN varchar,
    TITLE varchar,
    AUTHOR varchar,
    PUBLICATION_YR varchar,
    PUBLISHER varchar,
    IMG_URL_S varchar,
    IMG_URL_M varchar,
    IMG_URL_L varchar,
    PRIMARY KEY (isbn)
  );
  COPY books FROM '/data/BX-Books-Cleansed.csv'
    DELIMITERS ';' HEADER CSV;

  CREATE TABLE users(
    ID varchar,
    LOCATION varchar,
    AGE varchar,
    PRIMARY KEY(id)
  );
  COPY users (id, location, age) FROM '/data/BX-Users-Cleansed.csv'
    DELIMITERS ';' HEADER CSV;

  CREATE TABLE ratings(
    ID varchar,
    ISBN varchar,
    RATING smallint,
    CONSTRAINT isbn FOREIGN KEY (isbn) REFERENCES books(isbn),
    CONSTRAINT id FOREIGN KEY (id) REFERENCES users(id)
  );
  COPY ratings FROM '/data/BX-Book-Ratings-Cleansed.csv'
    DELIMITERS ';' HEADER CSV;

EOSQL
