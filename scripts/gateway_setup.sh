#!/bin/bash

set -e 

sudo ufw --force enable
sudo ufw default deny incoming 
sudo ufw allow 22/tcp
sudo ufw allow 8081/tcp

sudo apt-get update -y
sudo apt-get install -y python3-venv
sudo apt install npm -y
sudo npm install pm2@latest -g 

cat << end > /home/vagrant/api-gateway-app/.env
API_GATEWAY_PORT= $API_GATEWAY_PORT
API_GATEWAY_HOST=$API_GATEWAY_HOST
INVENTORY_PORT=$INVENTORY_PORT
INVENTORY_IP=$INVENTORY_IP
RABBITMQ_USER=$RABBITMQ_USER
RABBITMQ_PASS=$RABBITMQ_PASS
RABBITMQ_HOST=$RABBITMQ_HOST
RABBITMQ_PORT=$RABBITMQ_PORT
RABBITMQ_QUEUE=$RABBITMQ_QUEUE
RABBITMQ_VHOST=$RABBITMQ_VHOST
end

cd /home/vagrant/api-gateway-app/
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python_path=$(which python3)
pm2 start server.py --name api_gateway  --interpreter $python_path
pm2 save
pm2 startup

