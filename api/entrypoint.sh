#!/bin/sh

python /app/manager.py db init

python /app/manager.py db migrate --message 'initial database migration'
python /app/manager.py db upgrade

python /app/manager.py run
