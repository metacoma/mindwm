{%- set p = inventory.parameters %}
{%- set freeplane_fifo_path = p.freeplane.scripts.fifo_control.fifo_path -%}
#/usr/bin/env bash

NODE_ID=$1
FREEPLANE_FIFO="/tmp/freeplane-${NODE_ID}.fifo"
TMUX_LOG="/tmp/tmux-${NODE_ID}.log"
CLEAR_LOG="/tmp/tmux-${NODE_ID}-clear.log"

INPUT_DATA="/tmp/${NODE_ID}_input_data.log"
OUTPUT_DATA="/tmp/${NODE_ID}_output_data.log"


cat ${TMUX_LOG} | sed -r 's/\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?m//g;' | sed 's/\r//'g | ansifilter > ${CLEAR_LOG}


head -n1 ${CLEAR_LOG} > ${INPUT_DATA}
sed '1d;$d' ${CLEAR_LOG} > ${OUTPUT_DATA}

{{ p.compiled_dir }}/context_match.py -i ${INPUT_DATA} -o ${OUTPUT_DATA} | tee -a ${FREEPLANE_FIFO}


#grep -q "tmux ls" ${INPUT_DATA} && {
#    cat ${OUTPUT_DATA} | bash ~/_mindwm/adapters/tmux.sh >> ${FREEPLANE_FIFO}
#}
#
#grep -q ifconfig ${INPUT_DATA} && {
#  grep -q "Link encap" ${OUTPUT_DATA} && {
#    cat ${OUTPUT_DATA} | bash ~/_mindwm/adapters/ifconfig_nixos.sh >> ${FREEPLANE_FIFO}
#  }
#  grep -q ": flags" ${OUTPUT_DATA} && {
#    cat ${OUTPUT_DATA} | bash ~/_mindwm/adapters/ifconfig_ubuntu.sh | tee -a ${FREEPLANE_FIFO}
#  }
#  exit
#} 

