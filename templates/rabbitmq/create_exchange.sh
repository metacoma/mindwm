{%- set p = inventory.parameters %}
#!/usr/bin/env bash

RABBITMQ_ENDPOINT=`minikube ip`:{{ p.rabbitmq_manage_node_port }}

{% if "rabbitmq_exchanges" in p %}
{% for exchange_name, exchange in p.rabbitmq_exchanges.items() %}
kubectl -n {{ p.rabbitmq_namespace }} exec {{ p.rabbitmq_release_name }}-0 -ti -- curl -i -u {{ p.rabbitmq_user }}:{{ p.rabbitmq_password }} -H "Content-type: application/json" -XPUT -d'{{ exchange | to_json }}' localhost:15672/api/exchanges/%2f/{{ exchange_name }}
{% endfor %} {# for exchange_name, exchange in rabbitmq_exchanges.items() #}
{% endif %}

