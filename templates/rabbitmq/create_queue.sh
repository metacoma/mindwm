{%- set p = inventory.parameters %}
#!/usr/bin/env bash

RABBITMQ_ENDPOINT=`minikube ip`:{{ p.rabbitmq_manage_node_port }}

{% if "rabbitmq_queues" in p %}
{% for queue_name, queue in p.rabbitmq_queues.items() %}
kubectl -n {{ p.rabbitmq_namespace }} exec {{ p.rabbitmq_release_name }}-0 -ti -- curl -i -u {{ p.rabbitmq_user }}:{{ p.rabbitmq_password }} -H "Content-type: application/json" -XPUT -d'{{ queue | to_json }}' localhost:15672/api/queues/%2f/{{ queue_name }}
{% endfor %} {# for exhcnage_name, queue in rabbitmq_queues.items() #}
{% endif %}

