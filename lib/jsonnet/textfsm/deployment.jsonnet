local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

// computed imports are not allowed. :(
//local k8s_path = "files/github.com/jsonnet-libs/k8s-libsonnet" + "1.23" + "/main.libsonnet";
//local k8s = import k8s_path;

local k8s = import "files/github.com/jsonnet-libs/k8s-libsonnet/1.23/main.libsonnet";

local k8s_deployment(name, spec) =
  local deployment = k8s.apps.v1.deployment.new(name=name, containers=[
    k8s.core.v1.container.new(name="consumer", image=spec.image.repo+":"+spec.image.tag) +
        k8s.core.v1.container.withEnvMap({
            'KAFKA_BOOTSTRAP_SERVER': p.kafka_cluster_name + "-kafka-external-bootstrap." + p.kafka_k8s_namespace + ":" + p.kafka_port
        }) + k8s.core.v1.container.withImagePullPolicy("Never")
  ]);
  // TODO(@metacoma) fix p.textfsm.namespace
  deployment + k8s.apps.v1.deployment.metadata.withNamespace(p.textfsm.k8s_namespace);


{
  ["deployment"]: k8s_deployment(p.textfsm.k8s_deployment, p.textfsm)
}


