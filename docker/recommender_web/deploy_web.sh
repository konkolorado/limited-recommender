docker run -d \
    --name recommender_web -p 8000:8000 \
    --mount type=bind,src=$(pwd)/../../data/,dst=/data,readonly \
    --link postgres:postgres \
    recommender_web
