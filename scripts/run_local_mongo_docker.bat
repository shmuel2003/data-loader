@echo off
REM Run local MongoDB in Docker (no auth) for dev/testing
REM Data persisted in a local named volume: mongo_data

set VOLUME_NAME=mongo_data

docker volume create %VOLUME_NAME%

docker run -d --name mongo \
    -p 27017:27017 \
    -v %VOLUME_NAME%:/data/db \
    --restart unless-stopped \
    mongo:7.0

echo MongoDB is starting on mongodb://localhost:27017