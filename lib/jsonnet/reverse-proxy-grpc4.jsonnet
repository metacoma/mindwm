local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

local k8s = import "files/github.com/jsonnet-libs/k8s-libsonnet/1.23/main.libsonnet";

local k8s_reverse_grpc_proxy4_deployment(name, gproxy4_spec) =
  local deployment = k8s.apps.v1.deployment.new(name=name, containers=[
    k8s.core.v1.container.new(name="reverse-grpc-proxy4", image=p.gproxy4_container_image) +
        //k8s.core.v1.container.withImagePullPolicy("Never") +
	k8s.core.v1.container.withCommand(["/bin/sh"]) +
	k8s.core.v1.container.withArgs(["-c",
		gproxy4_spec.proxy_to.shell + "\n" +
 		p.gproxy4_container_entrypoint]
	) +
	{ env: gproxy4_spec.env } +
	{ ports: [ { containerPort: p.gproxy4_container_port } ] }

  ]);
  deployment + k8s.apps.v1.deployment.metadata.withNamespace(gproxy4_spec.namespace);

{
	[gproxy4]: k8s_reverse_grpc_proxy4_deployment(gproxy4, p.kubernetes["reverse-grpc-proxy4"][gproxy4]) for gproxy4 in std.objectFieldsAll(p.kubernetes["reverse-grpc-proxy4"])
}
