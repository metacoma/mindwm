local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

// computed imports are not allowed. :(
//local k8s_path = "files/github.com/jsonnet-libs/k8s-libsonnet" + "1.23" + "/main.libsonnet";
//local k8s = import k8s_path;

local k8s = import "files/github.com/jsonnet-libs/k8s-libsonnet/1.23/main.libsonnet";

local k8s_deployment(name, consumer_spec) = 
  local deployment = k8s.apps.v1.deployment.new(name=name, containers=[
    k8s.core.v1.container.new(name="consumer", image=p.consumer_image.repo_prefix + name)
  ]);
  deployment + k8s.apps.v1.deployment.metadata.withNamespace(p.kafka.k8s.consumer_namespace);


{
  [consumer_name + "/deployment"]: k8s_deployment(consumer_name, p.kafka.consumers[consumer_name]) for consumer_name in std.objectFieldsAll(p.kafka.consumers)
}


  //[consumer_name]: kubernetes_deployment(consumer_name) for consumer_name in std.objectFieldsAll(p.kafka.consumers)
//  [consumer_name + "/deployment.yaml"]: kubernetes_deployment(consumer_name) for consumer_name in std.objectFieldsAll(p.kafka.consumers)
