local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

local k8s = import "files/github.com/jsonnet-libs/k8s-libsonnet/1.23/main.libsonnet";

local generate_service(name, namespace, selector) =
  k8s.core.v1.service.new(
    name=name,
    selector={
      "name": selector,
    },
    ports=[{"port": p.gproxy4_container_port, "targetPort": p.gproxy4_container_port}]
  ) + k8s.core.v1.service.metadata.withNamespace(namespace);

{
	[gproxy4 + "-svc"]: generate_service(p.kubernetes["reverse-grpc-proxy4"][gproxy4].svc.name, p.kubernetes["reverse-grpc-proxy4"][gproxy4].namespace, gproxy4) for gproxy4 in std.objectFieldsAll(p.kubernetes["reverse-grpc-proxy4"])
}
