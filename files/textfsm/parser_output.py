import sys
import textfsm
import pprint
import json
from tabulate import tabulate
import io
from neo4j import GraphDatabase
import grpc
import freeplane_pb2
import freeplane_pb2_grpc
import pika
import pprint

template = sys.argv[1]
output_file = sys.argv[2]

rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"
neo4j_url = "bolt://192.168.49.2:31237"
neo4j_username = 'neo4j'
neo4j_password = 'password'

exchange_name = "io-document"

connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

grpc_channel = grpc.insecure_channel('localhost:50051')
fp = freeplane_pb2_grpc.FreeplaneStub(grpc_channel)

def do_textfsm(stdout):
    print(stdout)
    with open(template) as f:
        re_table = textfsm.TextFSM(io.StringIO(f.read()))
        header = re_table.header
        result = re_table.ParseText(stdout)
        # pprint.pprint(json.dumps(result))
        print(json.dumps({"header": header, "result": result}))
        #print(tabulate(result, headers=header))
        return header, result

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
def fpDrawTable(fp_node_id, tmux_pane_id, session_name, header, table_body):
    for item in table_body:
        fp_node = fp.CreateChild(freeplane_pb2.CreateChildRequest(name=item[0], parent_node_id = fp_node_id))
        name = item[0]

        cmd = "kubectl -n mindwm exec -ti %s -- /bin/sh" % (item[0])

        groovy_code = """
def post = new URL("http://192.168.49.2:31398/event").openConnection();
def message = '{"cmd":"%s", "tmux_pane_id": "%s", "session_name": "%s"}'
post.setRequestMethod("POST")
post.setDoOutput(true)
post.setRequestProperty("Content-Type", "application/json")
post.getOutputStream().write(message.getBytes("UTF-8"));
def postRC = post.getResponseCode();
println(postRC);
if (postRC.equals(200)) {
    println(post.getInputStream().getText());
    }
""" % (cmd,tmux_pane_id,session_name)

        fp.NodeAttributeAdd(freeplane_pb2.NodeAttributeAddRequest(node_id=fp_node.node_id, attribute_name='script1', attribute_value=groovy_code))
        for i in range(1, len(item)):
            fp.NodeAttributeAdd(freeplane_pb2.NodeAttributeAddRequest(node_id=fp_node.node_id, attribute_name=header[i], attribute_value=item[i]))
            print(f"{header[i]}: {item[i]}\n")



def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    io_context_document = IoContextDocument(data)
    original_string = io_context_document.getOutput()

    lines = original_string.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    result_string = "\n".join(non_empty_lines)

    header, result = do_textfsm(result_string)
    tmux_pane_id = data['metadata']['tmux']['pane_id']
    session_name = data['metadata']['tmux']['session_name']
    fpDrawTable(data['_fp_node_id'], tmux_pane_id, session_name, header, result)

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()

