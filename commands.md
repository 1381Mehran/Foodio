pip freeze > requirements.txt
python manage.py check
python manage.py startapp admin
python manage.py makemigrations
python manage.py migrate
