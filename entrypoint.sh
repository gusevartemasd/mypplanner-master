#!/bin/sh

if [[ ! -z "${DATABASE_URL}" ]]; then
    echo "Waiting for database ..."

    DB_HOST=`echo ${DATABASE_URL} | sed -r 's/.*@([^:]+):.*/\1/'`
    DB_PORT=`echo ${DATABASE_URL} | sed -r 's/.*@[^:]+:([^\/]+*)\/.*/\1/'`

    echo "Database hostname: ${DB_HOST}, port: ${DB_PORT}"

    while ! nc -z "${DB_HOST}" ${DB_PORT};
    do
        sleep 0.1;
    done;

    echo "Database started"

    ./manage.py migrate
    ./manage.py load_articles
    ./manage.py load_equipments
    ./manage.py load_deliveries
fi

gunicorn --config config/gunicorn.py config.wsgi:application
nginx -g "pid /tmp/nginx.pid; daemon off;"
