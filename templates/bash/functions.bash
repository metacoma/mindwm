#!/bin/bash
{% set p = inventory.parameters %}
{% set bash_functions = p.bash.functions %}

export KAPITAN_ROOT="{{ p.kapitan_root }}"
export KAPITAN_TARGET="{{ p.target_name }}"
export KAPITAN_COMPILED_DIR="{{ p.compiled_dir }}"

{% if "env" in p.bash %}
{% set bash_env = p.bash.env %}
{% for k,v in bash_env.items() %}
export {{ k }}="{{ v }}"
{% endfor %}
{% endif %}


{% if "alias" in p.bash %}
{% set alias = p.bash.alias %}
{% for k,v in alias.items() %}
alias {{ k }}="{{ v }}"
{% endfor %}
{% endif %}



{% for func,cmd in bash_functions.items() %}
{{ func }}() {
  {{ cmd }}
}
{% endfor %}

