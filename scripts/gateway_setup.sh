#!/bin/bash

set -e 

sudo ufw enable 
sudo ufw default deny incoming 
sudo ufw allow 22/tcp
sudo ufw allow 8081/tcp

sudo apt-get update -y
sudo apt-get install -y python3-venv
sudo apt install npm -y
sudo npm install pm2@latest -g 

tee << end > /home/vagrant/api-gateway-app/.env

API_GATEWAY_PORT= $API_GATEWAY_PORT
API_GATEWAY_HOST=$API_GATEWAY_HOST
RABBITMQ_USER=$RABBITMQ_USER
RABBITMQ_PASS=$RABBITMQ_PASS
RABBITMQ_HOST=$RABBITMQ_HOST
RABBITMQ_PORT=$RABBITMQ_PORT
RABBITMQ_QUEUE=$RABBITMQ_QUEUE
RABBITMQ_VHOST=$RABBITMQ_VHOST

end

cd /home/vagrant/api-gateway-app/
python3 -m venv envs
source ./envs/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python_path=$(which python3)
pm2 start server.py --name api_gateway  --interpreter $python_path

