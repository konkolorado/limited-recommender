docker stop web
docker rm web
./build_web.sh
./deploy_web.sh
docker logs -f web
