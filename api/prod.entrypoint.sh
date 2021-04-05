#!/bin/sh
# These commands are here because they must be run at runtime

python /app/manager.py db init

python /app/manager.py db migrate --message 'initial database migration'
python /app/manager.py db upgrade

gunicorn manager:app -b 0.0.0.0:5000
