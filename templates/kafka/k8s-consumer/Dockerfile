{% set p = inventory.parameters %}
FROM {{ p.base_image.repo}}:{{p.base_image.tag }}

{% if "python" in consumer %}
RUN apk add --update \
   python3           \
   py3-pip

RUN pip3 install kafka-python grpcio

ADD ./consumer /usr/local/bin/entrypoint.py
ENTRYPOINT ["python3", "/usr/local/bin/entrypoint.py"]
{% endif %}

# TODO(@metacoma) add GRPC protobuf files and compile

