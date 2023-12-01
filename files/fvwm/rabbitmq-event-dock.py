import pika
import pprint
import json
import re
import libtmux
import os
import subprocess
import base64
from collections import deque

class FixedSizeQueue:
      def __init__(self, max_size):
          self.queue = deque(maxlen=max_size)

      def add_element(self, element):
          self.queue.append(element)

      def get_elements(self):
          return list(self.queue)

idx = 0
max_size = 10
my_queue = FixedSizeQueue(max_size)

rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"

connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = "events"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

def display_message(message):
    command = f'echo "{message}" | bash /home/bebebeko/mindwm/compiled/fvwm/bin/aosd_show.sh'
    subprocess.run(command, shell=True)

def updateFvwmDock():
    fvwmDataHead = """
    DestroyModuleConfig FvwmButtons: *
    *FvwmButtons: Fore Black
    *FvwmButtons: Back rgb:90/80/90
    *FvwmButtons: Geometry -0-5
    *FvwmButtons: Rows 1
    *FvwmButtons: BoxSize smart
    *FvwmButtons: Font -*-helvetica-medium-r-*-*-12-*
    *FvwmButtons: Padding 2 2
    """
    fvwmBody = ""
    i = 0
    for element in my_queue.get_elements():
        decoded_string = base64.b64decode(element['event']['clipboard']).decode("utf-8")
        with open(f"/tmp/buffer{i}.txt", 'w') as file:
          file.write(decoded_string)
        fvwmBody = fvwmBody + f"""
        *FvwmButtons: (Title {decoded_string[15:]}, Icon /tmp/buttons/copy.png,  Action exec exec xterm -e "vim -R /tmp/buffer{i}.txt")
        """
        print("XXX " + decoded_string[15:])
        i = i + 1
    fvwmDataEnd = """
    KillModule FvwmButtons FvwmButtons
    Module FvwmButtons FvwmButtons
    Style FvwmButtons NoTitle
    """

    fvwmData = fvwmDataHead + fvwmBody + fvwmDataEnd

    process = subprocess.Popen(["bash", "/home/bebebeko/mindwm/compiled/fvwm/bin/fvwm_send.sh"], stdin=subprocess.PIPE)
    process.communicate(input = fvwmData.encode())
    process.wait()

def callback(ch, method, properties, body):
    global idx
    pprint.pprint(body.decode())
    print(json.loads(body.decode())['event'])
    my_queue.add_element(json.loads(body.decode()))
    updateFvwmDock()


rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
