{%- set p = inventory.parameters -%}
#!/usr/bin/env bash

NODE_ID=$1

test -z "${NODE_ID}" && {
  cat<<EOF > /dev/stderr
usage $0 \${NODE_ID}
for exmaple:
$0 ID_1090958577
EOF
  exit 1
} 

cd {{ p.kapitan_root }}

NEW_KTARGET_NAME="fp-shell-${NODE_ID}"
test -d inventory/targets/freeplane-nodes-sh || mkdir -p inventory/targets/freeplane-node-sh
# inventory/targets/freeplane-node.yml used as a template 
# use jq for this
cat inventory/targets/freeplane-node.yml | sed "
  s,target_name: .*,target_name: ${NEW_KTARGET_NAME},;
" | tee inventory/targets/freeplane-node-sh/${NEW_KTARGET_NAME}.yml

./kapitan.sh compile --fetch --cache -t ${NEW_KTARGET_NAME}
. compiled/${NEW_KTARGET_NAME}/functions.bash
TMUXINATOR_CONFIG={{ p.kapitan_root }}/compiled/${NEW_KTARGET_NAME} tmuxinator start --name ${NEW_KTARGET_NAME} --no-attach tmuxinator
