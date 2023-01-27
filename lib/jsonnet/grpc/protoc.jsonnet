local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  [grpc_name + ".proto"]: kap.jinja2_template("templates/grpc/raw.protoc", {
        inventory: inventory,
        protoc: p.grpc[grpc_name].protoc_raw
  }) for grpc_name in std.objectFieldsAll(p.grpc)
}

