#!/usr/bin/env bash

. ${KAPITAN_COMPILED}/bash/mindwm.sh

NODE_ID="$1"
TMUX_SESSION="Freeplane-Node-${NODE_ID}"

TMUX_LOGFILE="${MINDWM_TMP}/"

test -d mkdir -p 

rm ${TMUX_LOGFILE}
mkfifo ${TMUX_LOGFILE}
mkfifo "/tmp/freeplane-${NODE_ID}.fifo"

tmux has-session -t ${TMUX_SESSION} || ( 
  tmux new -s ${TMUX_SESSION} -d 'bash'
  #tmux pipe-pane -t ${TMUX_SESSION} "stdbuf -o0 sed -r 's/\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?m//g;' > ${TMUX_LOGFILE}"
  tmux new-window -t ${TMUX_SESSION}:1 -n shell
  tmux send-keys -t ${TMUX_SESSION}:0 "export PS1='\u@\h:\w\$ '" ENTER
  tmux send-keys -t ${TMUX_SESSION}:1 "export PS1='\u@\h:\w\$ '" ENTER
#  tmux send-keys -t ${TMUX_SESSION}:0 "/home/bebebeko/mindwm/compiled/mindwm//shell/tmux_fifo.groovy ${NODE_ID}" ENTER
  tmux pipe-pane -IO -t ${TMUX_SESSION}:1 "cat > ${TMUX_LOGFILE}"
  #tmux pipe-pane -I -t ${TMUX_SESSION} "cat > ${TMUX_LOGFILE}-stdout"
  sleep 5
)

tmux attach -t ${TMUX_SESSION} 
