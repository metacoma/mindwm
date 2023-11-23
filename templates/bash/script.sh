{%- set p = inventory.parameters %}
#!/usr/bin/env bash

set -eo pipefail

. {{ p.compiled_dir }}/functions.bash

{{ script }}
