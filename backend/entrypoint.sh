#!/bin/sh
set -e

echo "Waiting for postgres at ${POSTGRES_HOST}:${POSTGRES_PORT} ..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - continuing"

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Create superuser if credentials provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

# Start the server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

