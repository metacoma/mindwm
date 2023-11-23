import pika
import pprint
import json
import re
import libtmux
import os
import subprocess

rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = "events"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

def display_message(message):
    command = f'echo "{message}" | bash /home/bebebeko/mindwm/compiled/fvwm/bin/aosd_show.sh'
    subprocess.run(command, shell=True)

def callback(ch, method, properties, body):
    pprint.pprint(body.decode())
    display_message(body.decode())

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
