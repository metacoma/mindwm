{%- set p = inventory.parameters -%}
#!/usr/bin/env python
import argparse
import os
import re
from subprocess import Popen, PIPE


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--stdin", required=True,
                  help="file with stdin data")

ap.add_argument("-o", "--stdout", required=True,
                  help="file with stdout data")

args = vars(ap.parse_args())

with open(args['stdin'], 'r') as file:
        stdin_data = file.read()

with open(args['stdout'], 'r') as file:
        stdout_data = file.read()


#print(stdin_data)

{%- for ctx in p.context %}

input_match = 0
output_match = 0

{% if 'input' in ctx %}

input_p = re.compile("{{ ctx.input }}")
input_match = input_p.match(stdin_data)

{% endif %}

{% if 'output' in ctx %}
output_match = []
output_p = re.compile("{{ ctx.output }}")
for line in stdout_data.split("\n"):
  m = output_p.match(line)
  if (m):
    output_match.append(m)
{% endif %}

if (
{% if 'input' in ctx %}
   input_match
{% endif %}
{% if 'input' in ctx and 'output' in ctx %}
   and
{% endif %}
{% if 'output' in ctx %}
   len(output_match)
{% endif %}
  ): 

{% if "groovy" in ctx %}

  if (input_match): 
    for k,v in input_match.groupdict().items():
      # TODO(metacoma) change to groovy_set(key_name, val_name) -> print("%(key)s = '%(value)s'\n" % {'key': k, 'value': v})
      print("%(key)s = '%(value)s'\n" % {'key': k, 'value': v})
{% if 'output' in ctx %}
  if (len(output_match)): 
    for m in output_match:
      for k,v in m.groupdict().items():
        print("%(key)s = '%(value)s'\n" % {'key': k, 'value': v})
{% endif %} {# if 'output in ctx #}

  print('''
stdin_data = """
%(stdin_data)s
"""
stdout_data = """
%(stdout_data)s
"""
{{ ctx.groovy }}
''' % { 'stdin_data' : stdin_data, 'stdout_data':  stdout_data})
{%- endif -%} {# groovy #}
{% if "shell" in ctx %} 
  file_path = "/tmp/context_shell%(pid)s.bash" % { 'pid': os.getpid() }
  f = open(file_path, "w")
  f.write("""#!/usr/bin/env bash
  {# TODO(metacoma) set these env variables in others parts, like groovy #}
export KAPITAN_ROOT="${KAPITAN_ROOT:%(kapitan_root)s}"
export KAPITAN_TARGET="${KAPITAN_TARGET:%(kapitan_target)s}"
export KAPITAN_COMPILED="${KAPITAN_COMPILED:%(kapitan_compiled)s}"

  {# TODO(metacoma) set regex-match environment variables #}
  
test -f ${KAPITAN_COMPILED}/function.bash &&
  . ${KAPITAN_COMPILED}/function.bash
""" % {
      {# TODO(metacoma) fixture #}
  	'kapitan_root': 'KAPITAN_ROOT',
  	'kapitan_target': 'KAPITAN_TARGET',
  	'kapitan_compiled': 'KAPITAN_COMPILED',  {# '{{ inventory.kapitan.compiled_target_dir }}', #}
  })
  
  if (input_match): 
    for k,v in input_match.groupdict().items():
      f.write("export %(key)s = '%(value)s'\n" % {'key': k, 'value': v})
{% if 'output' in ctx %}
  if (len(output_match)): 
    for m in output_match:
      for k,v in m.groupdict().items():
        f.write("export %(key)s = '%(value)s'\n" % {'key': k, 'value': v})
{% endif %} {# if 'output in ctx #}


  f.write('''
{{ ctx.shell }}
  ''')
  f.close()
  with Popen(['bash', '-c', 'cat %(stdout_file)s | bash %(file_path)s' % {'stdout_file': args['stdout'], 'file_path': file_path}], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
        print(line, end='')
{% endif %} {# if "shell" in ctx #}


{%- endfor -%} {# for ctx in context #} 
