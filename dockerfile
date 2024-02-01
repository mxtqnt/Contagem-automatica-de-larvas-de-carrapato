FROM python:3.11-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements and install psycopg2 dependencies
COPY ./requirements.txt /requirements.txt
RUN apk update
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Creates a directory app in the container and copy the current directory to the container
WORKDIR /app
COPY . /app
