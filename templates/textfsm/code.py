{% set p = inventory.parameters %}
import re
import json
import pprint
import os
import tabulate
import textfsm
import io
from tabulate import tabulate
from kafka import KafkaConsumer
from kafka import KafkaProducer

bootstrap_server = os.environ.get('KAFKA_BOOTSTRAP_SERVER', '{{ p.kafka_cluster_name }}-kafka-external-0.{{ p.kafka_k8s_namespace }}:{{ p.kafka_port }}')

# TODO(@metacoma) parametrize input topic
consumer = KafkaConsumer('tmux-pane-io-context', bootstrap_servers=[bootstrap_server])

producer = KafkaProducer(bootstrap_servers=[bootstrap_server], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

patterns = dict()

{% for ctx in p["io-context"] %}
patterns["{{ ctx.input }}"] = re.compile("{{ ctx.input }}")
{% endfor %}

for message in consumer:
    msg = json.loads(message.value)
    pprint.pprint(msg)
    try:
        input_data = msg['message']['input']
        output_data = msg['message']['output']
    except KeyError:
        print("KeyError")
        continue
{% for ctx in p["io-context"] %}
    if (patterns["{{ ctx.input }}"].match(input_data)):
        textfsm_template="""{{ ctx.textfsm }}"""
        re_table = textfsm.TextFSM(io.StringIO(textfsm_template))
        header = re_table.header
        try:
            result = re_table.ParseText(output_data)
            print(tabulate(result, headers=header))
        except textfsm.parser.TextFSMError:
            continue
        msg.setdefault("metadata", {})['textfsm'] = result
        # msg["metadata"]["textfsm"] = result
        producer.send('mindwm-objects', value = msg)
{% endfor %}
