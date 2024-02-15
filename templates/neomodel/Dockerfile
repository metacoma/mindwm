FROM alpine:latest
RUN apk add --update \
	py3-pip	     \
	graphviz-dev \
	alpine-sdk
ADD . /processing/
WORKDIR /processing
RUN pip3 install -r ./requirements.txt
ENTRYPOINT [ "python3", "/processing/processing.py" ]

