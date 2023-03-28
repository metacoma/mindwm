{% set p = inventory.parameters %}
import re
import json
import pprint
import os
import tabulate
from kafka import KafkaConsumer
from kafka import KafkaProducer

consumer = KafkaConsumer('tmux-pane-io-context', bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER']])

patterns = dict()

{% for ctx in p["io-context"] %}
patterns["{{ ctx.input }}"] = re.compile("{{ ctx.input }}")
{% endfor %}

for message in consumer:
    msg = json.loads(message.value)
    try:
        intput_data = msg['input']
        output_data = msg['output']
    except KeyError:
        print("KeyError")
        continue
{% for ctx in p["io-context"] %}
    if (patterns["{{ ctx.input }}"].match(input_data)):
        template="""{{ctx.textfsm}}"""
        re_table = textfsm.TextFSM(io.StringIO(textfsm_template))
        result = re_table.ParseText(output_data)
        print(tabulate(result, headers=header))
{% endfor %}
