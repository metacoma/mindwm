local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

local pre = [
 'alias pane_title="printf \'\\033]2;%s\\033\\\\\' $1"'
];

{
  "tmuxinator": p.tmuxinator
}

