local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;


{
  [helm_name]: p.helm[helm_name] for helm_name in std.objectFieldsAll(p.helm) 
}
