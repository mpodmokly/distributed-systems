import pika
import sys
import json
from keys import EXCHANGE, ADMIN_KEY, SUPPLIER_KEY


if len(sys.argv) != 4:
    print("Invalid arguments")
    sys.exit(1)

agency_name = sys.argv[1]
services = sys.argv[2:]

order_no = 0
received_orders = set()

def callback_order(ch, method, properties, body):
    global order_no
    data = json.loads(body)
    
    if not data["id"] in received_orders:
        order_no += 1
        received_orders.add(data["id"])
    
    print(f"Realizing order {order_no}...")
    print(f"agency: {data["agency"]}")
    print(f"product: {data["product"]}")

    confirmation = {
        "type": "confirmation",
        "supplier": agency_name,
        "agency": data["agency"],
        "product": data["product"]
    }
    ch.basic_publish(
        exchange="",
        routing_key=data["agency"],
        body=json.dumps(confirmation)
    )
    ch.basic_publish(
        exchange="",
        routing_key=ADMIN_KEY,
        body=json.dumps(confirmation)
    )

    print("Confirmation sent\n")
    ch.basic_ack(method.delivery_tag)

def callback_msg(ch, method, properties, body):
    message = json.loads(body)
    print(f"Admin message: {message}")
    ch.basic_ack(method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.exchange_declare(EXCHANGE, exchange_type="direct")
channel.basic_qos(prefetch_count=1)

for product in services:
    channel.queue_declare(product)
    channel.basic_consume(product, callback_order)

queue = channel.queue_declare("", exclusive=True)
queue_name = queue.method.queue
channel.queue_bind(queue_name, EXCHANGE, routing_key=SUPPLIER_KEY)
channel.basic_consume(queue_name, callback_msg)

print(f"Supplier {agency_name} ready: {services}\n")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Supplier closed")
    channel.stop_consuming()
    connection.close()
