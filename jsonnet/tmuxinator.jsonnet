local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

// unused ATM
local pre = [
 'alias pane_title="printf \'\\033]2;%s\\033\\\\\' $1"'
];

local arrayIf(arr, condition) = if condition then arr else [];


//
//std.join("\n", [std.join("\n", nestedArray) for nestedArray in pre])
local generate_pre(pre) =
   if std.type(pre) == "array" then
   	if std.type(pre[0]) == "array" then
		std.join("\n", [std.join("\n", nestedArray) for nestedArray in pre])
	else 
		std.join("\n", pre)
   else if std.type(pre) == "string" then
   	pre
   else
	"XXX";



{
  "tmuxinator": {
    name: p.target_name,
    root: p.compiled_dir,
    windows: if std.objectHas(p.tmuxinator, "windows") then [
        {
	    [window_name]: {
	       pre: "source " + p.compiled_dir + "/functions.bash\n" + if std.objectHas(p.tmuxinator.windows[window_name], "pre") then generate_pre(p.tmuxinator.windows[window_name]["pre"]) else "YY",
	    	panes: p.tmuxinator.windows[window_name].panes
	    }
	} for window_name in std.objectFieldsAll(p.tmuxinator.windows)
    ] else []
  }
}

