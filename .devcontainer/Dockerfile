FROM mcr.microsoft.com/devcontainers/python:3

RUN python -m pip install --upgrade pip setuptools

COPY requirements.txt requirements.txt
COPY .devcontainer/requirements-dev.txt requirements-dev.txt
RUN python -m pip install -r requirements.txt -r requirements-dev.txt \
    && rm requirements.txt requirements-dev.txt
