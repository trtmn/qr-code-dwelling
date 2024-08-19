docker build -t qr-maker .
docker container stop qr-maker
docker container rm qr-maker
docker run -p 1337:8000 -v ./:/app --name qr-maker --env OP_SERVICE_ACCOUNT_TOKEN=${OP_SERVICE_ACCOUNT_TOKEN} -d --pull missing qr-maker:latest
docker image prune -f
docker container prune -f