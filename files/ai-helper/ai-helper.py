import pika
import pprint
import json
import re
from neo4j import GraphDatabase

rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"
neo4j_url = "bolt://192.168.49.2:31237"
neo4j_username = 'neo4j'
neo4j_password = 'password'

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = "io-line"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

def get_last_io_document(host, tmux_session_name, tmux_pane_id, n):
    query = """
MATCH (host:Node {node_type: "host", name: "%s"})-[:HAS_TMUX_SESSION]->(session:Node {node_type: "tmux_session", name: "%s"})-[:HAS_PANE]->(pane:Node {node_type: "tmux_pane", name: "%d"})-[:HAS_IO_CONTEXT]->(io_context:Node {node_type: "io_context"})-[:IO_DOCUMENT]->(io_document:Node {node_type: "io_document"})
WITH io_document
ORDER BY ID(io_document) DESC
LIMIT %d
RETURN io_document
""" % (host, tmux_session_name, int(tmux_pane_id), int(n))
    print(query)
    with GraphDatabase.driver(neo4j_url, auth=(neo4j_username, neo4j_password)) as driver:
        with driver.session() as session:
            result = session.run(query)
            record = result.single()
            return record

    return None


def callback(ch, method, properties, body):
    data = json.loads(body.decode())

    # trigger pattern
    # <user>@host:/home/user $ # ai request
    pattern = r".*@.*\$ #.*"
    if re.match(pattern, data['message']):
        host = data['host']
        tmux_session_name = data['metadata']['tmux']['session_name']
        tmux_pane_id = data['metadata']['tmux']['pane_id']
        last_document = get_last_io_document(host, tmux_session_name, tmux_pane_id, 1)
        cmd_input = last_document['io_document'].get('name')
        cmd_output = last_document['io_document'].get('output_data')

        question = re.sub(r'^.*?#[ ]?', '', data['message'])
        data = {
            "tmux_pane_id": tmux_pane_id,
            "tmux_session_name": tmux_session_name,
            "host": host,
            "question": question,
            "terminal-command-sequence": [{
                "input": cmd_input,
                "output": cmd_output
            }]
        }
        rabbitmq_channel.basic_publish(exchange='openai', routing_key='openai', body=json.dumps(data))
        pprint.pprint(data)

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
