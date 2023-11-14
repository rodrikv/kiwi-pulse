FROM python:3.11-slim

# setup
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y apt-utils
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN apt-get install -y \
    build-essential \
    python3 \
    python3-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libxml2 \
    gcc \
    libpq-dev


WORKDIR /code
COPY requirements.txt /code

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8000