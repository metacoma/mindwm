{%- set p = inventory.parameters -%}
#!/usr/bin/env python
import re
import argparse


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
{%- if 'input' in ctx -%}
   input_match
{%- endif -%}
{%- if 'input' in ctx and 'output' in ctx -%}
  and 
{%- endif -%}
{%- if 'output' in ctx -%}
   len(output_match)
{%- endif -%}
  ): 

{% if "groovy" in ctx %}

  if (input_match): 
    for k,v in input_match.groupdict().items():
      print("%(key)s = '%(value)s'\n" % {'key': k, 'value': v})
{% if 'output' in ctx %}
  if (len(output_match)): 
    for m in output_match:
      for k,v in m.groupdict().items():
        print("%(key)s = '%(value)s'\n" % {'key': k, 'value': v})
{% endif %}

  
    #print("def %(key) = '%(value)'" % {'key': k, 'value': v})

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

{%- endfor -%}
