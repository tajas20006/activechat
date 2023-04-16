# ActiveChat

Chat system that starts talking actively.

## developing

1. `poetry install`
1. `poetry run pre-commit install`

## testing

1. copy `.env.example` to `.env`

## zundamon server

### start

1. get image

    ```bash
    docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
    ```

1. start server

    ```bash
    docker run --rm \
      -p '127.0.0.1:50021:50021' \
      --name zundamon -d \
      voicevox/voicevox_engine:cpu-ubuntu20.04-latest
    ```

### get in docker ip address

1. `docker inspect zundamon | sls IPAddress`
1. update environment variable `ZUNDAMON_SERVER`

### stop

1. `docker stop zundamon`

## slack

### get api token

1. create channel
1. create app
1. add scopes

    1. chat:write
    1. files:read
    1. files:wirte
    1. incoming-webhook

1. copy API_TOKEN
1. add app to channel
1. update environment variable `SLACK_API_TOKEN`
