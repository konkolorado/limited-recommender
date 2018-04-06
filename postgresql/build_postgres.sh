docker build -f dockerfile.postgres -t postgres:current .

docker rmi postgres:latest
docker tag postgres:current postgres:latest
docker rmi postgres:current
