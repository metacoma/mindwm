import re
import pyte
import json
import pprint
from kafka import KafkaConsumer
from kafka import KafkaProducer

# https://bugzilla.redhat.com/show_bug.cgi?id=1914843

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


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))
# To consume latest messages and auto-commit offsets

consumer = KafkaConsumer('tmux-raw-stream',
#                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])

prompt_regex = re.compile(r'.*@.*[\$#] ')
ctx_input = {}
ctx_output = {} 

context = {}

for message in consumer:
    msg = json.loads(message.value) 
    session_name = msg["tags"][0]; # tmux.tmux-fp-shell-ID_898073125.fifo

    raw_line = escape_ansi(msg["message"])

    if (prompt_regex.match(raw_line)):
      if (      
           session_name in ctx_input and
           len(ctx_input[session_name]) and
           session_name in ctx_output and
           len(ctx_output[session_name])
         ):
        # print("FIRE THE EVENT!")
        producer.send('io-context', value = {
          'sesion_name': session_name,
          'input': ctx_input[session_name],
          'output': ctx_output[session_name]
        })
        ctx_input[session_name] = ""
      # new command
      print("PROMPT ->>> " + raw_line)
      ctx_input[session_name] = raw_line
      ctx_output[session_name] = []
    else: 
      if session_name in ctx_output:
        ctx_output[session_name].append(raw_line)



# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)
