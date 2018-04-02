pip3 freeze > requirements.txt

# This order allows you to keep the number of images minimal
docker build -f dockerfile.tests -t recommender-tests-image:current .

docker rmi recommender-tests-image:latest
docker tag recommender-tests-image:current recommender-tests-image:latest
docker rmi recommender-tests-image:current

docker run --rm --name recommender-tests recommender-tests-image:latest
