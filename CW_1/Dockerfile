FROM python:3.11.8-alpine3.19


WORKDIR /celery

# ensure Python output is sent directly to the terminal without buffering

ENV PYTHONNUNBUFFERED 1

# prevent python from writing .pyc files

ENV PYTHONDONTWRITEBYTECODE 1

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt



