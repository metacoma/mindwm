{% set p = inventory.parameters %}
{% set mindwm_consumer = p.mindwm.clipboard %}
# main import
{% for import_line in p.mindwm_clipboard.import %}
{{ import_line }}
{% endfor %}
{% for consumer_name, consumer in mindwm_consumer.items() %}
# import from {{ consumer_name }}
{% if "import" in consumer %}
{% for import_line in consumer.import %}
{{ import_line }}
{% endfor %}
{% endif %}
{% endfor %}


{{ p.mindwm_clipboard.init }}


connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))

#properties = pika.BasicProperties(
#            app_id="clipboard-consumer"
#)

rabbitmq_channel = connection.channel()

def new_event(exchange_name, queue_name, payload):
    return rabbitmq_channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=json.dumps(payload))

def getClipboardText(event):
    return base64.b64decode(event['payload']['clipboard']).decode('utf-8')

def debug(msg):
    print(msg)

{% for consumer_name, consumer in mindwm_consumer.items() %}
# init from {{ consumer_name }}
{% if "init" in consumer %}
{{ consumer.init }}
{% endif %}
{% endfor %}



{% for consumer_name, consumer in mindwm_consumer.items() %}
def {{ consumer_name }}_callback(ch, method, properties, body):
  event = json.loads(body)
  pprint.pprint(event)
  {{ consumer.callback | indent(2) }}

rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback={{ consumer_name }}_callback, auto_ack=True, consumer_tag = "clipboard")
{% endfor %}


print("Waiting for messages. To exit, press Ctrl+C")
rabbitmq_channel.start_consuming()

