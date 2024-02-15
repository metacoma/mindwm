{% set p = inventory.parameters %}
import pika
import pprint
import json
import os
from neomodel import config
from neo4j import GraphDatabase

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, One)

rabbitmq_url = os.getenv("RABBITMQ_URL")
neo4j_url = os.getenv("NEO4J_URL")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

config.DRIVER = GraphDatabase().driver(neo4j_url, auth=(neo4j_username, neo4j_password))

connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = "io-context"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

{% for class_name, class_data in p.knowledge_graph.items() %}
# {{ class_name }}
class {{ class_name }}(StructuredNode):
{% for property_name, property in class_data.items() %}
    {{ property_name -}} =
{%- if "type" in property and property.type|lower == "string" %}StringProperty()
{% elif "rel_to" in property %}
RelationshipTo('{{ property.rel_to.class }}', '{{ property.rel_to.type }}')
{% endif %}
{% endfor %}
{% endfor %}

def callback(ch, method, properties, body):
    {{ processing.code | indent(4) }}

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()


