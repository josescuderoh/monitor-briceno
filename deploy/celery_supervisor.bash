#!/bin/sh

# Wrapper script for running celery with virtualenv and env variables set

VENVDIR=/home/ubuntu/projects/monitor-briceno
DJANGODIR=$VENVDIR/monitor-briceno-proj/src/monitor_briceno

echo "Starting celery with args $@"

# Activate the virtual environment.
cd $VENVDIR
. monitor_venv/bin/activate

# Programs meant to be run under supervisor should not daemonize themselves
# (do not use --daemon).
cd $DJANGODIR
exec celery --app=monitor_briceno worker -B --loglevel=info
