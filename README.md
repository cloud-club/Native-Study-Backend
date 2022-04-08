# Prerequisite

- python >=3.8, <3.9
- poetry stable(1.1.13)

# Installation

## 1. Clone project

```
git clone https://github.com/cloud-club/Native-Study-Backend.git
cd Native-Study-Backend
```

## 2. Install [poetry](https://python-poetry.org/docs/)

### osx / linux

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### window

```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

## 3. Install python dependency

```
poetry install --no-dev
```

## 4. Generate env file and Write env

```
cp .env.example .env
```

# Run Service

## local

```
cd .../Native-Study-Backend
python3 main.py
```

## docker

```
docker-compose build
docker-compose up -d
```

## Open Swagger-ui

- http://localhost/docs

## Open Redoc-ui

- http://localhost/redoc

# Reference

- [fastapi](https://fastapi.tiangolo.com/)
- [poetry](https://python-poetry.org/docs/)
- [pre-commit](https://pre-commit.com/)
