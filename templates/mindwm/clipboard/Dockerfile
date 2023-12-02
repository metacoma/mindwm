FROM python:3.8-slim AS image

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV TWITCH_DL_VERSION=2.1.3-1-g268c99d

RUN apt-get update
RUN apt-get install -y python3 python3-pip build-essential python3-venv

ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
ADD ./code.py /usr/local/bin/code.py

CMD python3 /usr/local/bin/code.py

