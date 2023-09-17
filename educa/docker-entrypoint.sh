./wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT}

echo "Apply database migrations"
python manage.py migrate

echo "Start server"
gunicorn educa.wsgi:application --bind 0.0.0.0:8000 --forwarded-allow-ips="*"
#gunicorn educa.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver