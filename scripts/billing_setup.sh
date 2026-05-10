set -e 


sudo apt-get install rabbitmq-server -y --fix-missing

sudo apt install postgresql postgresql-contrib -y

sudo sudo -u postgres psql  << EOF
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER USER myuser CREATEDB;
CREATE DATABASE mydb OWNER myuser;
EOF
