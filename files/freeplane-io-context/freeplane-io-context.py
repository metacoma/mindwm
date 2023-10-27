{%- raw -%}
import pika
import pprint
import json
import freeplane_pb2
import freeplane_pb2_grpc
import grpc
import re
import os
from neo4j import GraphDatabase

#rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"
#neo4j_url = "bolt://192.168.49.2:31237"
#neo4j_username = 'neo4j'
#neo4j_password = 'password'

rabbitmq_url = os.getenv("RABBITMQ_URL")
neo4j_url = os.getenv("NEO4J_URL")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")
freeplane_grpc4_endpoint = os.getenv("FREEPLANE_GRPC4_ENDPOINT")

FP_DETAILS_MAX_LINE = 4

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

output_queue_name = "io-document"

exchange_name = os.getenv('EXCHANGE_NAME')
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

def check_relationship_exists(src, dst, relationship_type):
    query = (
        f"MATCH (s:Node {src}) "
        f"MATCH (d:Node {dst}) "
        f"RETURN EXISTS((s)-[:{relationship_type}]->(d)) AS relationshipExists"
    )
    print(query)

    with GraphDatabase.driver(neo4j_url, auth=(neo4j_username, neo4j_password)) as driver:
        with driver.session() as session:
            result = session.run(query)
            record = result.single()
            return record['relationshipExists']

class IoContext:

    _grpc_channel = {}
    _fp = {}
    _neo4j = {}
    _document = {}
    _session = {}

    # STUB
    def __clear_mindmap(self):
        print("TODO Clear mindmap")

    def sessionSetCurrentContextNode(self, current_context_node):
        sessionId = self._document.getUniqSessionId();
        if (sessionId not in self._session):
            self._session[sessionId] = {}
        self._session[sessionId]['current_context_node'] = current_context_node


    def sessionGetCurrentContextNode(self):
        sessionId = self._document.getUniqSessionId();
        if not sessionId in self._session:
            return None
        return self._session[sessionId]['current_context_node']

    def sessionSetCurrentIODocument(self, current_context_node):
        sessionId = self._document.getUniqSessionId();
        if (sessionId not in self._session):
            self._session[sessionId] = {}
        self._session[sessionId]['current_io_document'] = current_context_node

    def sessionGetCurrentIODocument(self):
        sessionId = self._document.getUniqSessionId();
        if not sessionId in self._session:
            return ""
        return self._session[sessionId]['current_io_document']

    def __init_fp(self):
        self._grpc_channel = grpc.insecure_channel(freeplane_grpc4_endpoint)
        self._fp = freeplane_pb2_grpc.FreeplaneStub(self._grpc_channel)

    def __init_neo4j(self):
        self._neo4j = GraphDatabase.driver(neo4j_url, auth=(neo4j_username, neo4j_password))

    def __clear_neo4j_db(self):
        q = """
            MATCH (n)
            DETACH DELETE (n)
        """
        with self._neo4j.session() as session:
            result = session.run(q)

    def __init__(self):
        # Neo4j
        self.__init_neo4j()
        self.__clear_neo4j_db()

        # FreePlane
        self.__init_fp()
        self.__clear_mindmap()

    def __node_type_exists(self, node_name, node_type):
        assert(node_name)
        assert(node_type)

        q = f"""
            MATCH (N) WHERE (N.name = '{node_name}' AND N.node_type = '{node_type}')
            RETURN N
        """
        with self._neo4j.session() as session:
            result = session.run(q)
            return result.single()

    def __neo4j_cypher(self, data):
        return re.sub(r'(?<!: )"(\S*?)"', '\\1', json.dumps(data))


    def __node_create(self, node_name, node_type, attrs):
        assert(node_name)
        assert(node_type)

        if attrs is None or attrs == "":
            attrs = {}
        attrs.update({"name": node_name, "node_type": node_type})
        # pprint.pprint(attrs)
        cypher_data = self.__neo4j_cypher(attrs)

        q = f"""
            CREATE (N:Node {cypher_data})
            RETURN (N)
        """
        print(q)
        with self._neo4j.session() as session:
            result = session.run(q)
            return result.single()

    def __neo4j_relationship_create(self, src, dst, relationship_type):

        #src_cypher = self.__neo4j_cypher(src)
        #dst_cypher = self.__neo4j_cypher(dst)

        query = (
                "MATCH (SRC), (DST) "
                f"WHERE (({src}) AND ({dst})) "
                f"CREATE (SRC)-[:{relationship_type}]->(DST) "
        )
        print(query)

        with GraphDatabase.driver(neo4j_url, auth=(neo4j_username, neo4j_password)) as driver:
            with driver.session() as session:
                result = session.run(query)
                record = result.single()
                return record


    def host_exists(self, hostname):
        return self.__node_type_exists(hostname, 'host')

    def getFPnodeId(self, node_name, node_type):
        host = self.__node_type_exists(node_name, node_type)
        return host['N'].get('_fp_node_id')

    def fpGetHostId(self, hostname):
        return self.getFPnodeId(hostname, 'host')

    def fpGetTmuxSessionId(self, tmux_session):
        return self.getFPnodeId(tmux_session, 'tmux_session')


    def host_create(self, hostname):
        fp_node = self._fp.CreateChild(freeplane_pb2.CreateChildRequest(name=hostname, parent_node_id = ''))
        self._fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id = fp_node.node_id, red =  176, green = 188, blue = 245, alpha = 255))
        self._fp.NodeDetailsSet(freeplane_pb2.NodeDetailsSetRequest(node_id=fp_node.node_id, details='Host'))
        return self.__node_create(hostname, 'host', {"_fp_node_id": fp_node.node_id })

    def parse_host(self, hostname):
        if not self.host_exists(hostname):
            self.host_create(hostname)

    def tmux_session_exists(self, tmux_session_name):
        return self.__node_type_exists(tmux_session_name, 'tmux_session')

    def tmux_session_create(self, tmux_session_name):

        fp_node = self._fp.CreateChild(freeplane_pb2.CreateChildRequest(name=tmux_session_name, parent_node_id = self.fpGetHostId(self._document.getHost())))
        self._fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id = fp_node.node_id, red =  0, green = 204, blue = 51, alpha = 255))
        self._fp.NodeDetailsSet(freeplane_pb2.NodeDetailsSetRequest(node_id=fp_node.node_id, details='tmux'))

        tmux_session_node = self.__node_create(tmux_session_name, 'tmux_session', {'_fp_node_id': fp_node.node_id})

        self.__neo4j_relationship_create(
            f"SRC.name = '{self._document.getHost()}' AND SRC.node_type = 'host'",
            f"DST.name = '{tmux_session_name}' AND DST.node_type = 'tmux_session'",
            "HAS_TMUX_SESSION"
        )

        return tmux_session_node


    def parse_tmux_session(self, session_name):
        if not self.tmux_session_exists(session_name):
            self.tmux_session_create(session_name)

    def tmux_pane_exists(self, tmux_pane_id):
        return self.__node_type_exists(tmux_pane_id, 'tmux_pane')

    def tmux_pane_create(self, tmux_pane_id):

        fp_node = self._fp.CreateChild(freeplane_pb2.CreateChildRequest(name=tmux_pane_id, parent_node_id = self.fpGetTmuxSessionId(self._document.getTmuxSessionName())))
        self._fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id = fp_node.node_id, red =  0, green = 0, blue = 247, alpha = 255))
        self._fp.NodeDetailsSet(freeplane_pb2.NodeDetailsSetRequest(node_id=fp_node.node_id, details='tmux pane'))

        tmux_pane_node = self.__node_create(tmux_pane_id, 'tmux_pane', {'_fp_node_id': fp_node.node_id})


        self.__neo4j_relationship_create(
            f"SRC.name = '{self._document.getTmuxSessionName()}' AND SRC.node_type = 'tmux_session'",
            f"DST.name = '{tmux_pane_id}' AND DST.node_type = 'tmux_pane'",
            "HAS_PANE"
        )

    def parse_tmux_pane(self, tmux_pane_id):
        if not self.tmux_pane_exists(tmux_pane_id):
            self.tmux_pane_create(tmux_pane_id)

    def fpGetParentContextNodeId(self, parentContext):
        if self.sessionGetCurrentContextNode() is None:
            return self.getFPnodeId(parentContext, 'tmux_pane')
        else:
            if (not self.isNewContext()):
                return self.sessionGetCurrentContextNode()['N'].get('_fp_node_id')
            else:
                return self.sessionGetCurrentIODocument()['N'].get('_fp_node_id')

    def io_context_create(self, io_context_name):

        fp_node = self._fp.CreateChild(freeplane_pb2.CreateChildRequest(name=io_context_name, parent_node_id = self.fpGetParentContextNodeId(self._document.getTmuxPaneId())))
        self._fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id = fp_node.node_id, red =  0, green = 153, blue = 153, alpha = 255))
        self._fp.NodeDetailsSet(freeplane_pb2.NodeDetailsSetRequest(node_id=fp_node.node_id, details='io context'))

        current_context_node = self.__node_create(io_context_name, 'io_context', {"_fp_node_id": fp_node.node_id})

        self.sessionSetCurrentContextNode(current_context_node)

        return current_context_node

    def lookup_parent_io_context(self):
        if (self.sessionGetCurrentContextNode() is None):
            q = '''
                MATCH (host:Node {{node_type: 'host', name: '{host}'}})-[:HAS_TMUX_SESSION]->(session:Node {{node_type: 'tmux_session', name: '{tmux_session_name}'}})-[:HAS_PANE]->(pane:Node {{node_type: 'tmux_pane', name: '{tmux_pane_id}'}})
            RETURN pane
            '''.format(
                host = self._document.getHost(),
                tmux_session_name = self._document.getTmuxSessionName(),
                tmux_pane_id = self._document.getTmuxPaneId()
            )
            with self._neo4j.session() as session:
                result = session.run(q)
                return result.single()['pane'].element_id
        else:
            return self.sessionGetCurrentContextNode()['N'].element_id



    def parse_io_context(self, ps1):
        with self._neo4j.session() as session:
            source_node_id = self.lookup_parent_io_context()
            io_context_node = self.io_context_create(ps1)
            assert(source_node_id != "")
            q = f'''
                MATCH (sourceNode)
                WHERE elementId(sourceNode) = '{source_node_id}'
                MATCH (targetNode)
                WHERE elementId(targetNode) = '{io_context_node['N'].element_id}'
                CREATE (sourceNode)-[:HAS_IO_CONTEXT]->(targetNode)
            '''
            result = session.run(q)
            return io_context_node


    def __neo4j_relationship_create(self, src, dst, relationship_type):

        #src_cypher = self.__neo4j_cypher(src)
        #dst_cypher = self.__neo4j_cypher(dst)

        query = (
                "MATCH (SRC), (DST) "
                f"WHERE (({src}) AND ({dst})) "
                f"CREATE (SRC)-[:{relationship_type}]->(DST) "
        )
        print(query)

        with GraphDatabase.driver(neo4j_url, auth=(neo4j_username, neo4j_password)) as driver:
            with driver.session() as session:
                result = session.run(query)
                record = result.single()
                return record


    def host_exists(self, hostname):
        return self.__node_type_exists(hostname, 'host')

    def getFPnodeId(self, node_name, node_type):
        host = self.__node_type_exists(node_name, node_type)
        return host['N'].get('_fp_node_id')

    def fpGetHostId(self, hostname):
        return self.getFPnodeId(hostname, 'host')

    def fpGetTmuxSessionId(self, tmux_session):
        return self.getFPnodeId(tmux_session, 'tmux_session')


    def host_create(self, hostname):
        fp_node = self._fp.CreateChild(freeplane_pb2.CreateChildRequest(name=hostname, parent_node_id = ''))
        self._fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id = fp_node.node_id, red =  176, green = 188, blue = 245, alpha = 255))
        self._fp.NodeDetailsSet(freeplane_pb2.NodeDetailsSetRequest(node_id=fp_node.node_id, details='Host'))
        return self.__node_create(hostname, 'host', {"_fp_node_id": fp_node.node_id })

    def parse_input_output(self, input_data, output_data):

        fp_node_details = output_data
        output = output_data.split('\r')


        if len(output) > FP_DETAILS_MAX_LINE:
            fp_node_details = "\r".join(output[:FP_DETAILS_MAX_LINE]) + "\r..."

        fp_node = self._fp.CreateChild(freeplane_pb2.CreateChildRequest(name=input_data, parent_node_id = self.sessionGetCurrentContextNode()['N'].get('_fp_node_id')))
        # fp_node = self._fp.CreateChild(freeplane_pb2.CreateChildRequest(name=input_data, parent_node_id = self.getIODocumentParentNode())
        self._fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id = fp_node.node_id, red =  176, green = 188, blue = 245, alpha = 255))
        self._fp.NodeDetailsSet(freeplane_pb2.NodeDetailsSetRequest(node_id=fp_node.node_id, details=fp_node_details))

        self._fp.NodeNoteSet(freeplane_pb2.NodeNoteSetRequest(node_id=fp_node.node_id, note="<BR>".join(output_data.split("\r"))))


        current_io_document = self.__node_create(input_data, 'io_document', {"_fp_node_id": fp_node.node_id, "output_data": output_data })
        self.sessionSetCurrentIODocument(current_io_document)

        source_node = self.sessionGetCurrentContextNode()['N'].element_id
        target_node = self.sessionGetCurrentIODocument()['N'].element_id

        with self._neo4j.session() as session:
            q = f'''
                MATCH (sourceNode)
                WHERE elementId(sourceNode) = '{source_node}'
                MATCH (targetNode)
                WHERE elementId(targetNode) = '{target_node}'
                CREATE (sourceNode)-[:IO_DOCUMENT]->(targetNode)
            '''
            result = session.run(q)


        return current_io_document


    def isNewContext(self):
        return self._document.getPS1Start() != self._document.getPS1End()

    def contextIsNotExists(self, ps1):
        current_context = self.sessionGetCurrentContextNode()
        assert(current_context is not None)
        q = f'''
            MATCH (M) WHERE elementId(M) = '{current_context['N'].element_id}'
            MATCH (N {{name: '{ps1}'}})
            MATCH (N)-[:HAS_IO_CONTEXT]->(M)
            RETURN N
        '''
        with self._neo4j.session() as session:
            result = session.run(q)
            node = result.single()
            return node

        return None


    def document(self, document):
        self._document = document
        documentId = self._document.getUniqSessionId()
        print(f"documentId: {documentId}")

        self.parse_host(self._document.getHost())
        self.parse_tmux_session(self._document.getTmuxSessionName())
        self.parse_tmux_pane(self._document.getTmuxPaneId())

        if (self.sessionGetCurrentContextNode() is None):
            self.parse_io_context(self._document.getPS1Start())

        self.parse_input_output(self._document.getInput(), self._document.getOutput())

        if (self.isNewContext()):
            existingContext = self.contextIsNotExists(self._document.getPS1End())
            if (existingContext is None):
                self.parse_io_context(self._document.getPS1End())
            else:
                self.sessionSetCurrentContextNode(existingContext)

        return self.sessionGetCurrentIODocument()

class IoContextDocument:
    __io_document = {}
    __host = ""
    __tmux_session_name = ""
    __tmux_pane_id = ""

    def getUniqSessionId(self):
        return 'mindwm-{hostname}-{tmux_session_name}-{tmux_pane_id}'.format(
            hostname = self.getHost(),
            tmux_session_name = self.getTmuxSessionName(),
            tmux_pane_id = self.getTmuxPaneId()
        )

    def getHost(self):
        return self.__io_document['host']

    def getTmuxSessionName(self):
        return self.__io_document['metadata']['tmux']['session_name']

    def getTmuxPaneId(self):
        return self.__io_document['metadata']['tmux']['pane_id']

    def getPS1Start(self):
        # fix for the new pane
        ps1 = self.__io_document['message']['ps1_start']
        if ps1 == '':
            ps1 = self.__io_document['message']['ps1_end']

        return ps1

    def getPS1End(self):
        return self.__io_document['message']['ps1_end']

    def getInput(self):
        return self.__io_document['message']['input']

    def getOutput(self):
        return self.__io_document['message']['output']

    def __init__(self, document):
        self.__io_document = document
        pprint.pprint(document)
        print(f"IoContextDocument: {self.getHost()}->{self.getTmuxSessionName()}")





def callback(ch, method, properties, body):
    data = json.loads(body.decode())

    io_context_document = IoContextDocument(data)

    neo4j_node = ioContext.document(io_context_document)
    data['neo4j_element_id'] = neo4j_node['N'].element_id
    data['_fp_node_id'] = neo4j_node['N'].get('_fp_node_id')

    rabbitmq_channel.basic_publish(exchange='io-document', routing_key='io-document', body=json.dumps(data))
    print(f"Published data to {output_queue_name}: {json.dumps(data)}")


ioContext = IoContext()
rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
{%- endraw -%}
