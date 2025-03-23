#!/bin/sh

#!/bin/sh

set -e

if [ -n "$DB_NAME" ] && [ "$DB_NAME" = "postgres" ]; then
    echo "Waiting for postgres..."

    host="${DB_HOST:-db}"
    port="${DB_PORT:-5432}"
    user="${DB_USER:-postgres}"

    until pg_isready -h "$host" -p "$port" -U "$user"; do
        sleep 0.1
    done

    echo "PostgreSQL is ready"
fi

# start cron
crond -l 0 -d 0 -L /home/website/logs/cron.log

# flush all data in the database
#python manage.py flush --no-input

# takes ORM models and makes the sql statements, we shouldn't need to do this since we're committing the migrations
python manage.py makemigrations --noinput

# applies migrations and creates/updates/deletes tables
python manage.py migrate --noinput

# collects static files
python manage.py collectstatic --no-input

exec "$@"
