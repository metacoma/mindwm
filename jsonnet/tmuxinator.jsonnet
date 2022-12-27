local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

// unused ATM
local pre = [
 'alias pane_title="printf \'\\033]2;%s\\033\\\\\' $1"'
];

local arrayIf(arr, condition) = if condition then arr else [];

{
  "tmuxinator": {
    name: p.target_name,
    root: p.compiled_dir,
    windows: [
      {
        [window_name]: {
	  pre: [
            "source " + p.compiled_dir + "/functions.bash"
          ] + arrayIf(p.tmuxinator.windows[window_name].pre, std.objectHas(p.tmuxinator.windows[window_name], "pre")),
          panes: p.tmuxinator.windows[window_name].panes,
        }
      } for window_name in std.objectFieldsAll(p.tmuxinator.windows)
    ]
  }
}

