import pika
import pprint
import json
import grpc
import re
import libtmux
import openai
import os
from neo4j import GraphDatabase

rabbitmq_url = "amqp://user:password@192.168.49.2:30466/%2f"
neo4j_url = "bolt://192.168.49.2:31237"
neo4j_username = 'neo4j'
neo4j_password = 'password'

openai.api_key = os.getenv("OPENAI_API_KEY")

FP_DETAILS_MAX_LINE = 4

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
rabbitmq_channel = connection.channel()

exchange_name = "openai"
result = rabbitmq_channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

rabbitmq_channel.queue_bind(exchange=exchange_name, queue=queue_name)

def callback(ch, method, properties, body):

    messages = [
        {"role": "system", "content":
        """I work in bash, enter commands, and receive responses in the form of text. The assistant is required to help me by answering my questions.
"""}
    ]
    pprint.pprint(body.decode())

    data = json.loads(body.decode())

    openai_payload = {
        "question": data['question'],
        "terminal-command-sequence": data['terminal-command-sequence']
    }

    messages.append({"role": "user", "content": json.dumps(openai_payload)})

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    tmux_pane_id = data['tmux_pane_id']
    tmux_session_name = data['tmux_session_name']

    # Print the response and add it to the messages list
    for i in range(len(response['choices'])):
      chat_message = response['choices'][i]['message']['content']
      print(f"Bot: #{i} {chat_message}")
#      tmux_cmd = {
#        "tmux_pane_id": "{tmux_pane_id}",
#        "session_name": "{tmux_session_name}",
#        "cmd": f"""cat<<OPENAI_EOF
#*************
#{chat_message}
#*************
#OPENAI_EOF
#"""
#      }

      tmux_cmd = {
        "tmux_pane_id": tmux_pane_id,
        "session_name": tmux_session_name,
        "cmd": f"""echo{chat_message}"""
      }
      rabbitmq_channel.basic_publish(exchange='tmux', routing_key='tmux', body=json.dumps(tmux_cmd))
      break

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()
