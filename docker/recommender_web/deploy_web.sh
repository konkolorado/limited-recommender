docker run -d \
    --name recommender_web -p 8000:8000 \
    --link postgres:postgres \
    recommender_web
