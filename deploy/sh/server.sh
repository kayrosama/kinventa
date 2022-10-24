#!/bin/bash
DJANGO_DIR=$(dirname $(dirname $(cd `dirname $0` && pwd)))
DJANGO_SETTINGS_MODULE=config.settings
cd $DJANGO_DIR
source $DJANGO_DIR/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
exec python manage.py runserver 0:1666
