from flask import request,Response,jsonify,Blueprint
from .config import Config
import requests
import pika

services_bp= Blueprint("services_bp",__name__)

def forward_to_inventory(url:str):
    try:
        headers = {}
        for key, value in request.headers:
            if key != "Host":
                headers[key] = value        
        resp=requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.data,
            cookies=request.cookies,
            allow_redirects=False
        )
        response = Response(resp.content, resp.status_code)
        for key, value in resp.headers.items():
            response.headers[key] = value

        return response
    except requests.exceptions.ConnectionError :
        return  jsonify({"message":"CONNECTION REFUSED"}),503
    
def billing_service():
    data=request.get_json()
    if not data:
        return jsonify({"message":"Request Body is required."}), 400
    
    required_fields=["user_id", "number_of_items","total_amount"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message":f"{field} is required."}), 400
    try:
        credential=pika.PlainCredentials(Config.RABBITMQ_USER,Config.RABBITMQ_PASS)
        params=pika.ConnectionParameters(host=Config.RABBITMQ_HOST,port=Config.RABBITMQ_PORT,credentials=credential,virtual_host=Config.RABBITMQ_VHOST)
        connection=pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True, arguments={'x-queue-type': 'quorum'})
        channel.basic_publish(exchange='',routing_key=Config.RABBITMQ_QUEUE,body=request.get_data())
        connection.close()
        return jsonify({"message":"message added to queue seccessfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Could not queue billing request: {str(e)}"}), 503
         


    
@services_bp.route("/<path:path>",methods=["GET","POST","DELETE","PUT"])
def server(path:str):
    
    if path.startswith("api/movies"):
        return forward_to_inventory(f"http://{Config.INVENTORY_IP}:{Config.INVENTORY_PORT}/{path}")
    elif path.startswith("api/billing"):
        if request.method != "POST":
            return jsonify({"message":"METHOD NOT ALLOWED"}), 405     

        return billing_service()
    else:
        return jsonify({"message":"SERVICE NOT FOUND"}), 404     
    
    