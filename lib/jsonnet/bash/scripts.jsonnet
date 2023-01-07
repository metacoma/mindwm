local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  [func_name + ".sh"]: kap.jinja2_template("templates/bash/script.sh", {
        inventory: inventory,
        script: p.bash.functions[func_name] + " $*"
  }) for func_name in std.objectFieldsAll(p.bash.functions)
}

