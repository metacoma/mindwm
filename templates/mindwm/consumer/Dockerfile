{%- set p = inventory.parameters -%}
{%- set is_python =  "python" in consumer or "python_code" in consumer or "python_requirements" -%}
FROM {{ consumer.base_image | default(p.mindwm_consumer_base_image) }}

{% if is_python -%}
RUN apk add --update 	\
	python3 	\
	py3-pip


{% if "python_requirements" in consumer -%}
RUN pip3 install {{ consumer.python_requirements | join(" ") }}
{%- endif -%} {# if "python_requirements" in consumer #}
{%- endif -%} {# if is_python #}

RUN mkdir /consumer
ADD ./consumer /consumer/
