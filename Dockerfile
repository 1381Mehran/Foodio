FROM python:3.11.8-alpine3.19

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8010

ENV PYTHONNUNBUFFERED 1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8010"]