#!/usr/bin/env bash

PIPE_DIR=${1}

for named_pipe_path in `find ${PIPE_DIR} -type p -printf "%f\n"`; do
  cat<<EOF
# TODO (@metacoma) use yaml config format for fluentd
# https://docs.fluentd.org/configuration/config-file-yaml
<source>
  @type named_pipe
  path ${PIPE_DIR}/${named_pipe_path}
  tag tmux.${named_pipe_path}
  format none
</source>
EOF

  
done

cat<<EOF
<match tmux.**>
  @type rawtcp
  #buffer_type file
  #buffer_path /var/log/fluent/logcentral
  <buffer>
     flush_mode interval
     #flush_mode immediate
     flush_interval 0.1
  </buffer>
  <server>
    name log1
    host ${LOGSTASH_HOST}
    port ${LOGSTASH_PORT}
  </server>
</match>
EOF
