#!/bin/sh

# Wrapper script for running celery with virtualenv and env variables set

VENVDIR=/usr/local/virtualenvs
DJANGODIR=/usr/local/apps/monitor-briceno-proj/src/monitor_briceno

echo "Starting celery..."

# Activate the virtual environment.
cd $VENVDIR
. monitor_venv/bin/activate

# Programs meant to be run under supervisor should not daemonize themselves
# (do not use --daemon).
cd $DJANGODIR
sudo exec celery --app=monitor_briceno worker -B --loglevel=info
