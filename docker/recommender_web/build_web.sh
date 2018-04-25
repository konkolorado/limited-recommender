pip3 freeze > requirements.txt

docker build -f dockerfile.web -t recommender_web:current .

docker rmi recommender_web:latest
docker tag recommender_web:current recommender_web:latest
docker rmi recommender_web:current
