set -e 

#install dependecies
sudo apt-get update -y

sudo apt-get install -y python3-venv

sudo apt install npm -y

sudo npm install pm2@latest -g 

sudo apt install postgresql postgresql-contrib -y

sudo -u postgres psql  << EOF
CREATE USER $USER_DB WITH PASSWORD '$PASSWORD_DB';
ALTER USER $USER_DB CREATEDB;
CREATE DATABASE billing_db OWNER $USER_DB;
EOF

sudo apt-get install rabbitmq-server -y --fix-missing


sudo rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASS

sudo rabbitmqctl set_permissions -p $RABBITMQ_VHOST $RABBITMQ_USER ".*" ".*" ".*"

sudo systemctl restart rabbitmq-server.service 

#create .env File

tee << end > /home/vagrant/billing-app/.env

BILLING_DATABASE_URL=$BILLING_DATABASE_URL
USER_DB=$USER_DB
PASSWORD_DB=$PASSWORD_DB
RABBITMQ_USER=$RABBITMQ_USER
RABBITMQ_PASS=$RABBITMQ_PASS
RABBITMQ_HOST=$RABBITMQ_HOST
RABBITMQ_VHOST=$RABBITMQ_VHOST
RABBITMQ_PORT=$RABBITMQ_PORT

end

cd /home/vagrant/billing-app
python3 -m venv envs
source ./envs/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python_path=$(which python3)
pm2 start server.py --name billing-app  --interpreter $python_path