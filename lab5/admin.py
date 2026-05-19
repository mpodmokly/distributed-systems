import pika
import json
import threading
from keys import EXCHANGE, ADMIN_KEY, SUPPLIER_KEY, AGENCY_KEY


def callback(ch, method, properties, body):
    data = json.loads(body)

    if data["type"] == "order":
        print(f"Order: {data["agency"]} -> {data["product"]}")
    elif data["type"] == "confirmation":
        info = f"Confirmation: {data["supplier"]} -> {data["agency"]}"
        info += f" -> {data["product"]}"
        print(info)
    
    ch.basic_ack(method.delivery_tag)

def communicator(ch):
    print("A <message> - message agencies")
    print("S <message> - message suppliers")
    print("U <message> - message all users")

    while True:
        try:
            command = input("Command:\n")
        except EOFError:
            print("STOP")
            break
        
        if len(command) <= 2:
            print("Wrong command")
            continue

        mode = command.split(" ")[0]
        if mode == "A":
            routing_key = AGENCY_KEY
        elif mode == "S":
            routing_key = SUPPLIER_KEY
        elif mode == "U":
            ch.basic_publish(
                exchange=EXCHANGE,
                routing_key=AGENCY_KEY,
                body=json.dumps(command[2:])
            )
            ch.basic_publish(
                exchange=EXCHANGE,
                routing_key=SUPPLIER_KEY,
                body=json.dumps(command[2:])
            )
            continue
        else:
            print("Wrong command")
            continue
        
        ch.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(command[2:])
        )


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.exchange_declare(EXCHANGE, exchange_type="direct")
channel.basic_qos(prefetch_count=1)

thread = threading.Thread(target=communicator, args=(channel,), daemon=True)
thread.start()

channel.queue_declare(ADMIN_KEY)
channel.basic_consume(ADMIN_KEY, callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Admin closed")
    channel.stop_consuming()
    connection.close()
