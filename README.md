# nomad-api-python

Playing around with the Nomad http API

## Requirements

- [Nomad](https://christopherbaklid.com/posts/nomad/)
- [Traefik](https://christopherbaklid.com/posts/traefik/)

## Setup

Prerequisites (Python 3.12)

```sh
apt install python3-poetry
poetry install
```

Environment variables

```sh
export NOMAD_TOKEN="some token if any"
export NOMAD_ADDR="http://127.0.0.1:4646"
```

## Run

```sh
make run
```
