docker run -d \
    --name web -p 8000:8000 \
    --mount type=bind,src=$(pwd)/../../data/,dst=/data,readonly \
    --link postgres:postgres \
    web:latest
