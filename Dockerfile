ARG UBUNTU_VERSION

FROM ubuntu:${UBUNTU_VERSION}

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TZ=Asian/Seoul \
    PYTHONPATH=$PATH:/workspace \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get -qq update
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install python3-pip \
    python3-venv \
    curl \
    tzdata \
    portaudio19-dev

# intsall poetry and python venv disable
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - && \
    ln -s $HOME/.poetry/bin/poetry /usr/bin/poetry && \
    poetry config virtualenvs.create false

RUN mkdir /workspace
WORKDIR /workspace
COPY . .

RUN poetry install

ENTRYPOINT [ "python3", "main.py" ]
