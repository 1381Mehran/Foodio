FROM python:3.11.8-alpine3.19

# Set working directory
WORKDIR /app

# Install bash
RUN apk add --no-cache bash

# Copy files
COPY . .

RUN ./venv.sh

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONNUNBUFFERED 1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]