\set PGBOOKS `echo $PGBOOKS`
\set PGUSERS `echo $PGUSERS`
\set PGRATINGS `echo $PGRATINGS`

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
COPY books FROM :'PGBOOKS'
  DELIMITERS ';' HEADER CSV;

CREATE TABLE users(
  ID varchar,
  LOCATION varchar,
  AGE varchar,
  PRIMARY KEY(id)
);
COPY users FROM :'PGUSERS'
  DELIMITERS ';' HEADER CSV;

CREATE TABLE ratings(
  ID varchar,
  ISBN varchar,
  RATING smallint,
  CONSTRAINT isbn FOREIGN KEY (isbn) REFERENCES books(isbn),
  CONSTRAINT id FOREIGN KEY (id) REFERENCES users(id)
);
COPY ratings FROM :'PGRATINGS'
  DELIMITERS ';' HEADER CSV;
