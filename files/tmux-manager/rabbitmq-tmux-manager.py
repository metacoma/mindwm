import pika
import pprint
import json
import re
import libtmux
import os

rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = "tmux"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

def callback(ch, method, properties, body):

    pprint.pprint(body.decode())
    tmux_cmd  = json.loads(body.decode())

    server = libtmux.Server()
    tmux_pane_id = tmux_cmd['tmux_pane_id']
    session_name = tmux_cmd['session_name']

    session = server.find_where({"session_name": session_name})
    session.panes.filter(pane_id = "%" + tmux_pane_id)[0].send_keys(tmux_cmd['cmd'])

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
