from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_GATEWAY_PORT=environ.get('API_GATEWAY_PORT')
    API_GATEWAY_HOST=environ.get('API_GATEWAY_HOST')
    BILLING_HOST=environ.get('BILLING_HOST')
    BILLING_PORT=environ.get('BILLING_PORT')
    
    INVENTORY_HOST=environ.get('INVENTORY_HOST')
    INVENTORY_IP=environ.get('INVENTORY_IP')
    INVENTORY_PORT=environ.get('INVENTORY_PORT')
    
    RABBITMQ_USER=environ.get("RABBITMQ_USER")
    RABBITMQ_PASS=environ.get("RABBITMQ_PASS")
    RABBITMQ_HOST=environ.get("RABBITMQ_HOST")
    RABBITMQ_PORT=environ.get("RABBITMQ_PORT")
    RABBITMQ_VHOST=environ.get("RABBITMQ_VHOST")
    RABBITMQ_QUEUE=environ.get("RABBITMQ_QUEUE")