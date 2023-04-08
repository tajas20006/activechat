# ActiveChat

Chat system that starts talking actively.

## developing

1. `poetry install`
1. `poetry run pre-commit install`

## testing

1. copy `.env.example` to `.env`

## zundamon server

### start

1. `docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest`
1. `docker run --rm -p '127.0.0.1:50021:50021' --name zundamon voicevox/voicevox_engine:cpu-ubuntu20.04-latest`

### get in docker ip address

1. `docker inspect zundamon | sls IPAddress`
1. update environment variable `ZUNDAMON_SERVER`

### stop

1. `docker stop zundamon`
