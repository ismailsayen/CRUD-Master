set -e 

echo "Updating packages..."
sudo apt-get update -y

echo "Installing dependencies..."
sudo apt-get install -y \
    python3-venv \
    npm \
    postgresql \
    postgresql-contrib \
    rabbitmq-server

echo "Installing PM2..."
sudo npm install -g pm2

sudo -u postgres psql  << EOF
CREATE USER $USER_DB WITH PASSWORD '$PASSWORD_DB';
ALTER USER $USER_DB CREATEDB;
CREATE DATABASE billing_db OWNER $USER_DB;
EOF



sudo rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASS || true

sudo rabbitmqctl set_permissions -p $RABBITMQ_VHOST $RABBITMQ_USER ".*" ".*" ".*" || true

sudo systemctl restart rabbitmq-server.service 

#create .env File

cat << end > /home/vagrant/billing-app/.env

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
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python_path=$(which python3)
pm2 start server.py --name billing-app  --interpreter $python_path
pm2 save
pm2 startup