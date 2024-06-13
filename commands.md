# Project

pip freeze > requirements.txt

python manage.py check

python manage.py startapp admin

python manage.py makemigrations

python manage.py migrate

# Docker Part

- up - docker-compose up -d --build

- down - docker-compose down

- Restart - docker-compose restart

# Linux Part

### to run composes in the same network 
- docker compose -f docker-compose-persistent.yml -f docker-compose.yml up
- alias dcd="docker compose -f docker-compose-persistent.yml -f docker-compose.yml down"

# RabbitMQ

### See list of queues in rabbit mq server with command :

- sudo rabbitmqctl list_queues

### See detail in rabbitmq server with cli

- sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged