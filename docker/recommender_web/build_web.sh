pip3 freeze > requirements.txt

docker build -f dockerfile.web -t web:current .

docker rmi web:latest
docker tag web:current web:latest
docker rmi web:current
