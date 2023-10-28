import pika
import pprint
import json
import grpc
import re
import libtmux
from neo4j import GraphDatabase

rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"
neo4j_url = "bolt://192.168.49.2:31237"
neo4j_username = 'neo4j'
neo4j_password = 'password'

FP_DETAILS_MAX_LINE = 4

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = "io-line"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

def callback(ch, method, properties, body):
    pprint.pprint(body.decode())
    #data = json.loads(body.decode())
    #pprint.pprint(data)
    #session_name = data['session_name']
    #tmux_pane_id = data['tmux_pane_id']
    #cmd = data['cmd']

    #server = libtmux.Server()

    #session = server.find_where({"session_name": session_name})
    #session.panes.filter(pane_id = "%" + tmux_pane_id)[0].send_keys(cmd)

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
