pip3 freeze > requirements.txt

docker build -f Dockerfile.tests -t recommender-tests-image .

# This order allows you to keep the number of images minimal
docker rmi recommender-tests-image:current
docker tag recommender-tests-image:latest recommender-tests-image:current

docker run --rm --name recommender-tests recommender-tests-image
