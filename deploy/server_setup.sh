#!/usr/bin/env bash

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/josescuderoh/monitor-briceno.git'

mkdir /home/ubuntu/projects
PROJECT_NAME='monitor-briceno'
PROJECT_BASE_PATH='/home/ubuntu/projects/$PROJECT_NAME'
VIRTUALENV_BASE_PATH='/home/ubuntu/projects/$PROJECT_NAME'

# Set Ubuntu Language
locale-gen es_ES.UTF-8

# Install Python, and pip
sudo
apt-get update
apt-get install -y python3-dev python-pip supervisor nginx git
apt-get install redis-server libgdal-dev

# Upgrade pip to the latest version.
sudo pip install --upgrade pip
sudo pip install virtualenv

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/monitor-briceno-proj

mkdir -p $VIRTUALENV_BASE_PATH
sudo virtualenv  $VIRTUALENV_BASE_PATH/monitor_briceno

source $VIRTUALENV_BASE_PATH/monitor_briceno/bin/activate
pip install -r $PROJECT_BASE_PATH/monitor-briceno-proj/requirements.txt

# Run migrations
cd $PROJECT_BASE_PATH/monitor-briceno-proj/src

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/monitor-briceno-proj/deploy/supervisor_monitor_briceno.conf /etc/supervisor/conf.d/monitor_briceno.conf
supervisorctl reread
supervisorctl update
supervisorctl restart monitor_briceno

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/monitor-briceno-proj/deploy/nginx_monitor_briceno.conf /etc/nginx/sites-available/monitor_briceno.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/monitor_briceno.conf /etc/nginx/sites-enabled/monitor_briceno.conf
systemctl restart nginx.service

echo "DONE! :)"
