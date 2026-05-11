
from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    BILLING_DATABASE_URL=environ.get("BILLING_DATABASE_URL")
    
    RABBITMQ_USER=environ.get("RABBITMQ_USER")
    RABBITMQ_PASS=environ.get("RABBITMQ_PASS")
    RABBITMQ_HOST=environ.get("RABBITMQ_HOST")
    RABBITMQ_PORT=environ.get("RABBITMQ_PORT")
    RABBITMQ_VHOST=environ.get("RABBITMQ_VHOST")    
    RABBITMQ_QUEUE=environ.get("RABBITMQ_QUEUE")
    











    