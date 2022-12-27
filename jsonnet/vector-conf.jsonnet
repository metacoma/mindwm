local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  [conf_name]: p.vector.config[conf_name] for conf_name in std.objectFieldsAll(p.vector.config)
}

