#!/bin/bash

# python collectstatic files
python manage.py collectstatic --no-input --settings=APPNAME.settings.production

# Adding migrations to database
python manage.py migrate --no-input --settings=APPNAME.settings.production

# Initializing supervisor
supervisord -c /etc/supervisor/supervisord.conf -n