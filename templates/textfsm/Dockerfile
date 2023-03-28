{% set p = inventory.parameters %}
{% set base_image = p.textfsm.base_image %}
FROM {{ base_image.repo}}:{{ base_image.tag }}

RUN apk add --update \
   python3           \
   py3-pip

RUN pip3 install kafka-python grpcio textfsm tabulate

ADD ./code.py /usr/local/bin/entrypoint.py
ENTRYPOINT ["python3", "/usr/local/bin/entrypoint.py"]
