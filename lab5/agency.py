import pika
import sys
import json
import uuid
from keys import EXCHANGE, ADMIN_KEY, AGENCY_KEY


agency_name = sys.argv[1]
services = sys.argv[2:]
counter = len(services)
order_id = uuid.uuid4()

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

def callback_confirmation(ch, method, properties, body):
    global counter
    data = json.loads(body)

    print(f"From {data["supplier"]}: {data["product"]}")
    counter -= 1

    if counter == 0:
        print("Order completed")
    
    ch.basic_ack(method.delivery_tag)

def callback_msg(ch, method, properties, body):
    message = json.loads(body)
    print(f"Admin message: {message}")
    ch.basic_ack(method.delivery_tag)


channel.exchange_declare(EXCHANGE, exchange_type="direct")
channel.basic_qos(prefetch_count=1)

channel.queue_declare(agency_name)
queue = channel.queue_declare("", exclusive=True)
queue_name = queue.method.queue

channel.queue_bind(queue_name, EXCHANGE, routing_key=AGENCY_KEY)
channel.basic_consume(agency_name, callback_confirmation)
channel.basic_consume(queue_name, callback_msg)

for product in services:
    order = {
        "type": "order",
        "id": str(order_id),
        "agency": agency_name,
        "product": product
    }

    print("Sending order...")
    channel.basic_publish(
        exchange="",
        routing_key=product,
        body=json.dumps(order)
    )
    channel.basic_publish(
        exchange="",
        routing_key=ADMIN_KEY,
        body=json.dumps(order)
    )
    
    print(f"agency: {agency_name}")
    print(f"product: {product}\n")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

    if counter != 0:
        print("Order not completed")

connection.close()
