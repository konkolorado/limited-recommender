docker build -f dockerfile.postgres -t postgres .

docker run -d --name postgres --mount type=bind,src=$(pwd)/data/,dst=/data postgres
