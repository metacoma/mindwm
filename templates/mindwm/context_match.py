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
output_p = re.compile("{{ ctx.output }}")
output_match = output_p.match(stdout_data)
{% endif %}

if (
{%- if 'input' in ctx -%}
   input_match
{%- endif -%}
{%- if 'input' in ctx and 'output' in ctx -%}
  and 
{%- endif -%}
{%- if 'output' in ctx -%}
   output_match
{%- endif -%}
  ): 

{% if "print" in ctx %}

  if (input_match): 
    for k,v in input_match.groupdict().items():
      print("def %(key)s = '%(value)s'\n" % {'key': k, 'value': v})

  if (output_match): 
    for k,v in output_match.groupdict().items():
      print("def %(key)s = '%(value)s'\n" % {'key': k, 'value': v})

  
    #print("def %(key) = '%(value)'" % {'key': k, 'value': v})

  print('''
def stdin_data = """
%(stdin_data)s
"""
def stdout_data = """
%(stdout_data)s
"""
{{ ctx.print }}
''' % { 'stdin_data' : stdin_data, 'stdout_data':  stdout_data})
{%- endif -%}

{%- endfor -%}
