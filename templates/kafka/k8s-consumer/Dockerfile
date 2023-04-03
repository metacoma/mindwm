{% set p = inventory.parameters %}
FROM {{ p.base_image.repo}}:{{p.base_image.tag }}

{% if "python" in consumer %}
RUN apk add --update \
   python3           \
   py3-pip

RUN pip3 install kafka-python

RUN mkdir /consumer
ADD ./consumer /consumer/consumer.py
{% if "grpc" in p and p.grpc.freeplane %}
RUN mkdir -p /consumer/
ADD ./freeplane.proto /consumer/
RUN pip3 install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I/consumer --python_out=/consumer/ --pyi_out=/consumer/ --grpc_python_out=/consumer/ /consumer/freeplane.proto
{% endif %}
ENTRYPOINT ["python3", "/consumer/consumer.py"]
{% endif %}
{% if "ruby" in consumer %}
RUN apk add --update \
  ruby               \
  ruby-dev           \
  build-base         \
  libffi-dev         \
  bash

RUN gem install grpc grpc-tools rdkafka
ADD ./consumer /usr/local/bin/entrypoint.rb
ENTRYPOINT ["ruby", "/usr/local/bin/entrypoint.rb"]
{% endif %}

# TODO(@metacoma) add GRPC protobuf pre-built files

