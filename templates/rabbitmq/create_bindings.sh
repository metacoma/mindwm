{%- set p = inventory.parameters %}
#!/usr/bin/env bash

RABBITMQ_ENDPOINT=`minikube ip`:{{ p.rabbitmq_manage_node_port }}

{% if "rabbitmq_bindings" in p %}
{% for binding_name, binding in p.rabbitmq_bindings.items() %}
kubectl -n {{ p.rabbitmq_namespace }} exec {{ p.rabbitmq_release_name }}-0 -ti -- curl -i -u {{ p.rabbitmq_user }}:{{ p.rabbitmq_password }} -H "Content-type: application/json" -XPOST -d'{{ binding.data | to_json  }}' localhost:15672/api/bindings/%2f/e/{{ binding.exchange_name }}/q/{{ binding.queue_name }}
{% endfor %} {# for binding_name, binding in rabbitmq_bindings.items() #}
{% endif %}

