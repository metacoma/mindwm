{% set p = inventory.parameters %}
{% if "env" in p.mindwm_clipboard %}
{% for env_name, env_key in p.mindwm_clipboard.env.items() %}
{{ env_name }} := {{ env_key }}
export {{ env_name }}
{% endfor %}
{% endif %}

image:
	docker build -t mindwm/clipboard:latest .
docker_run: image
	docker run \
        -ti 	   \
	--network=host \
{% if "env" in p.mindwm_clipboard %}
{% for env_name, env_key in p.mindwm_clipboard.env.items() %}
	-e {{ env_name }}='{{ env_key }}' \
{% endfor %}
{% endif %}
	mindwm/clipboard:latest
