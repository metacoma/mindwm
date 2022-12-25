import json
import hashlib
import os

def env_override(value, key):
  return os.getenv(key, value)



def to_json(string):
    return json.dumps(string)

def md5sum(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()

