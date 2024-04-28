FROM python:3.12.3-slim-bookworm

# Set working directory
WORKDIR /app

# Install bash
#RUN apk add --no-cache bash

# activate virtual Environment
COPY venv.sh /app

RUN chmod +x venv.sh

RUN source ./venv.sh

# Copy requirements.txt file

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

# copy rest remaining files

COPY . .

EXPOSE 8000

# ensure Python output is sent directly to the terminal without buffering

ENV PYTHONNUNBUFFERED 1

# prevent python from writing .pyc files

ENV PYTHONDONTWRITEBYTECODE 1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]