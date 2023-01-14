import re
import pyte
import json
import pprint
from kafka import KafkaConsumer
from kafka import KafkaProducer

# works fine, but VERY VERY SLOW
def pyte_fix(s):
  pyte_screen = pyte.Screen(240, 240)
  pyte_stream = pyte.ByteStream(pyte_screen)
  pyte_stream.feed(bytes(s, encoding='utf-8'))
  text = ("".join([line.rstrip() + "\n" for line in pyte_screen.display])).strip() + "\n"
  return text

ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
def escape_ansi(line):
  return ansi_escape.sub('', line)


consumer = KafkaConsumer('tmux-pane-raw-io-context',
                         bootstrap_servers=['minikube:30348'])

producer = KafkaProducer(bootstrap_servers=['minikube:30348'],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))

prompt_regex = re.compile(r'.*@.*[\$#] ')
ctx_input = {}
ctx_output = {} 

context = {}

for message in consumer:
    # ConsumerRecord(topic='tmux-pane-raw-io-context', partition=0, offset=107, timestamp=1673704934552, timestamp_type=0, key=None, value=b'{"host":"nixos","message":{"input":" pwd\\r","metadata":{"tmux_pane_id":"%32"},"output":"\\u001b[?2004l\\r/home/bebebeko/mindwm/compiled/vector\\r\\u001b[?2004h\\r\\r"},"source_type":"file_descriptor","timestamp":"2023-01-14T14:02:14.552293982Z","tmux_pane_id":"%32"}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=260, serialized_header_size=-1)
    msg = json.loads(message.value) 
    msg["message"]["output"] = escape_ansi(msg["message"]["output"])
    pprint.pprint(msg)
    producer.send('tmux-pane-io-context', value = msg) 



# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)
