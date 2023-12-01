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

#config.DRIVER = GraphDatabase().driver("bolt://192.168.49.2:31237", auth=('neo4j', 'password'))
config.DRIVER = GraphDatabase().driver(neo4j_url, auth=(neo4j_username, neo4j_password))

connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = os.getenv('EXCHANGE_NAME')
exchange_name = "io-context"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

class IoDocument(StructuredNode):
    input = StringProperty(required = True)
    output = StringProperty(required = True)
    io_context = RelationshipTo('IoContext', 'HAS_IO_CONTEXT')

class IoContext(StructuredNode):
    name = StringProperty(unique_index=True, required = True)
    io_document = RelationshipTo(IoDocument, 'HAS_IO_DOCUMENT')
    io_context = RelationshipTo('IoContext', 'HAS_IO_CONTEXT')

    def getLastIoDocument(self):
        # XXX refact
        nodes = self.io_document.filter()
        if (len(nodes)):
            return nodes[0]



class TmuxPane(StructuredNode):
    pane_id = IntegerProperty(required = True)
    io_context = RelationshipTo(IoContext, 'HAS_IO_CONTEXT')
    active_io_context = RelationshipTo(IoContext, 'ACTIVE_IO_CONTEXT')

    def switchActiveIoContext(self, active_context):
        self.active_io_context.disconnect_all()
        self.active_io_context.connect(active_context)

    def getActiveIoContext(self):
        nodes = self.active_io_context.filter()
        if (len(nodes)):
            return nodes[0]


class TmuxSession(StructuredNode):
    name = StringProperty(unique_index=True, required = True)
    pane = RelationshipTo(TmuxPane, 'HAS_TMUX_PANE')

class TmuxHost(StructuredNode):
    name = StringProperty(unique_index=True, required = True)
    session = RelationshipTo(TmuxSession, 'HAS_TMUX_SESSION')


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    pprint.pprint(data)


    host = TmuxHost.get_or_create(
        {
            "name": data['host']
        }
    )[0]

    tmux_session = host.session.get_or_none(name = data['metadata']['tmux']['session_name'])

    if (tmux_session is None):
        tmux_session = TmuxSession(name = data['metadata']['tmux']['session_name']).save()
        host.session.connect(tmux_session)

    pane = tmux_session.pane.get_or_none(pane_id = int(data['metadata']['tmux']['pane_id']))

    if (pane is None):
        pane = TmuxPane(pane_id = int(data['metadata']['tmux']['pane_id'])).save()
        tmux_session.pane.connect(pane)

    io_context = pane.getActiveIoContext()

    if io_context is None:
        io_context = IoContext(name = data['message']['ps1_start']).save()
        pane.io_context.connect(io_context)



    io_document = IoDocument(
        input = data['message']['input'],
        output = data['message']['output']
    ).save()


    if (data['message']['ps1_start'] != data['message']['ps1_end']):
        # context change
        print("New context")
        new_io_context = IoContext(name = data['message']['ps1_end']).save()
        pane.switchActiveIoContext(new_io_context)
        #io_context.io_context.connect(new_io_context)
        io_document.io_context.connect(new_io_context)
    else:
        #pane.getActiveIoContext().connect(io_context)
        pane.switchActiveIoContext(io_context)


    pane.getActiveIoContext().io_document.connect(io_document)

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
