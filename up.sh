# A simple script to start the docker containers

# PREREQUISITES:
# 1. Docker
# 2. Docker Compose (official version `docker compose`, not docker-compose)
# 3. ENV variables set for OP_SERVICE_ACCOUNT_TOKEN)
# 4 other variables in the service account vault.

# Find the location of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

docker compose -f ./docker-compose.yml -p qr-maker up --always-recreate-deps --remove-orphans --force-recreate -d --build
