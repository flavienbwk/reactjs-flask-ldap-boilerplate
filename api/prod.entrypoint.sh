#!/bin/sh
# These commands are here because they must be run at runtime

cd /app

python -m main db init
python -m main db migrate --message 'Initial database migration'
python -m main db upgrade

gunicorn main:app -b 0.0.0.0:5000
