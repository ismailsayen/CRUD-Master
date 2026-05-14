set -e

echo "Updating packages..."
sudo apt-get update -y

echo "Installing dependencies..."
sudo apt-get install -y \
    python3-venv \
    npm \
    postgresql \
    postgresql-contrib \


echo "Installing PM2..."
sudo npm install -g pm2

sudo -u postgres psql  << EOF
CREATE USER $USER_DB WITH PASSWORD '$PASSWORD_DB';
ALTER USER $USER_DB CREATEDB;
CREATE DATABASE movies_db OWNER $USER_DB;
EOF

cat << end > /home/vagrant/inventory-app/.env

INVENTORY_DATABASE_URL=$INVENTORY_DATABASE_URL
INVENTORY_PORT=$INVENTORY_PORT
INVENTORY_HOST=$INVENTORY_HOST

end

cd /home/vagrant/inventory-app
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python_path=$(which python3)
pm2 start server.py --name inventory-app --interpreter $python_path
pm2 save
pm2 startup