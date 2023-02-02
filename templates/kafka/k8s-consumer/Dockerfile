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

