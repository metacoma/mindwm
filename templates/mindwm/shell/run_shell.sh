{%- set p = inventory.parameters %}
#!/usr/bin/env bash

{{ p.terminal.emulator }} {{ p.compiled_dir }}/shell/tmux.sh $* &
