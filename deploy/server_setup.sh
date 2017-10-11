#!/usr/bin/env bash

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/josescuderoh/monitor-briceno.git'

PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'
# Set Ubuntu Language
# sudo locale-gen es_ES.UTF-8

# Install Python, and pip
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-virtualenv

#Create directories
sudo mkdir -p $PROJECT_BASE_PATH
sudo git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/monitor-briceno-proj

#Create and activate virtualenv
sudo mkdir -p $VIRTUALENV_BASE_PATH
sudo virtualenv -p python3  $VIRTUALENV_BASE_PATH/monitor_venv

source $VIRTUALENV_BASE_PATH/monitor_venv/bin/activate
sudo pip install -r $PROJECT_BASE_PATH/monitor-briceno-proj/requirements.txt

#Install requirements
sudo apt-get install python3-dev
sudo apt-get install redis-server
sudo apt-get install libgdal-dev

#Create executables for supervisor
cd $PROJECT_BASE_PATH/monitor-briceno-proj/deploy
sudo chmod +x gunicorn_start.bash
sudo chmod +x celery_supervisor.bash

#Install new requirements
sudo apt-get install supervisor
sudo apt-get install nginx

#Create log files
cd $PROJECT_BASE_PATH/monitor-briceno-proj
sudo mkdir log
cd log
sudo touch nginx-access.log
sudo touch nginx-error.log
sudo touch monitor_briceno.log
sudo touch monitor_briceno_err.log
sudo touch celery_default.out.log
sudo touch celery_default.err.log

# Setup Supervisor to run our uwsgi process.
sudo cp $PROJECT_BASE_PATH/monitor-briceno-proj/deploy/supervisor_monitor_briceno.conf /etc/supervisor/conf.d/monitor_briceno.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all

sudo chown -R ubuntu:ubuntu $VIRTUALENV_BASE_PATH/monitor_venv/run

# Setup nginx to make our application accessible.
sudo cp $PROJECT_BASE_PATH/monitor-briceno-proj/deploy/nginx_monitor_briceno.conf /etc/nginx/sites-available/monitor_briceno.conf
# sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/monitor_briceno.conf /etc/nginx/sites-enabled/monitor_briceno.conf
sudo service nginx start

echo "DONE! :)"
