# Prerequisite

- python >=3.8, <3.9
- poetry stable(1.1.13)

# Installation

## 1. clone project

```
git clone https://github.com/cloud-club/Native-Study-Backend.git
cd Native-Study-Backend
```

## 2. install [poetry](https://python-poetry.org/docs/)

### osx / linux

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### window

```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

## 3. install python dependency

```
poetry install --no-dev
```

# Run Service

```
cd .../Native-Study-Backend
python3 main.py
```

## Open Swagger-ui

- http://localhost:8080/docs

## Open Redoc-ui

- http://localhost:8080/redoc

# Reference

- [fastapi](https://fastapi.tiangolo.com/)
- [poetry](https://python-poetry.org/docs/)
- [pre-commit](https://pre-commit.com/)
