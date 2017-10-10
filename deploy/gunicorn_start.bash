#!/bin/bash

NAME="monitor_briceno"                                   # Name of the application
DJANGODIR=/usr/local/apps/monitor-briceno-proj/src/monitor_briceno               # Django project
SOCKFILE=/usr/local/virtualenvs/monitor_venv/run/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                         # the user to run as
GROUP=ubuntu                                        # the group to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=monitor_briceno.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=monitor_briceno.wsgi              # WSGI module name
echo "Starting $NAME as `whoami`"

# Make sure the virtual environment is activated

cd $DJANGODIR
source /usr/local/virtualenvs/monitor_venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONIOENCODING=UTF-8

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || sudo mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
