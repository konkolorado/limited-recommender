PGLOCAL=/tmp/pgdata
PGDATA=/var/lib/postgresql/data
mkdir -p $PGLOCAL

docker run -d \
    --name postgres \
    --mount type=bind,src=$(pwd)/../data/,dst=/data,readonly \
    --mount type=bind,src=$PGLOCAL,dst=$PGDATA\
    postgres
