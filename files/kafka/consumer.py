import re
import pyte
import json
import pprint
from kafka import KafkaConsumer

# https://bugzilla.redhat.com/show_bug.cgi?id=1914843

# works fine, but VERY VERY SLOW
def pyte_fix(s):
  pyte_screen = pyte.Screen(240, 240)
  pyte_stream = pyte.ByteStream(pyte_screen)
  pyte_stream.feed(bytes(s, encoding='utf-8'))
  text = ("".join([line.rstrip() + "\n" for line in pyte_screen.display])).strip() + "\n"
  return text

ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
def escape_ansi(line):
  return ansi_escape.sub('', line)


# To consume latest messages and auto-commit offsets

consumer = KafkaConsumer('tmux-events',
#                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])


for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    msg = json.loads(message.value) 
    print(escape_ansi(msg["message"]))
    #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
    #                                      message.offset, message.key,
    #                                      pyte_fix(message.value)))

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)
