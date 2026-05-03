import json
from .config import Config
from .model import db,Order
import pika

def callback(ch, method, properties, body):
        
        data =json.loads(body)
        # print(f" [x] Received {data['number_of_items']}")
        order = Order(
            user_id=data['user_id'],
            number_of_items=data['number_of_items'],
            total_amount=data['total_amount'],
        )
        
        db.session.add(order)
        db.session.commit()
        
        # ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consoming(app):
    credentials=pika.PlainCredentials(
        Config.RABBITMQ_USER,
        Config.RABBITMQ_PASS
        )
    
    params=pika.ConnectionParameters(
        host=Config.RABBITMQ_HOST,
        port=Config.RABBITMQ_PORT,
        virtual_host=Config.RABBITMQ_VHOST,
        credentials=credentials
        )
    connection=pika.BlockingConnection(params)
    channel=connection.channel()
    channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True, arguments={'x-queue-type': 'quorum'})   
     
    def ctxt_call(ch, method, properties, body):
        with app.app_context():
            callback(ch, method, properties, body)
            
    channel.basic_consume(queue=Config.RABBITMQ_QUEUE, on_message_callback=ctxt_call, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    