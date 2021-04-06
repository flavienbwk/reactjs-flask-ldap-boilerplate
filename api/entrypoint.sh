#!/bin/sh
# These commands are here because they must be run at runtime

pip install -e /app

set -x
python -m my_app db init
python -m my_app db migrate --message 'Initial database migration'
python -m my_app db upgrade
python -m my_app run
