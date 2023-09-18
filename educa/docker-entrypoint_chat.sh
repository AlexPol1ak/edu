./wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT}

echo "Apply database migrations"
python manage.py migrate

echo "Start chat server"
daphne -u daphne.sock educa.asgi:application
