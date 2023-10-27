local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

// computed imports are not allowed. :(
//local k8s_path = "files/github.com/jsonnet-libs/k8s-libsonnet" + "1.23" + "/main.libsonnet";
//local k8s = import k8s_path;

local k8s = import "files/github.com/jsonnet-libs/k8s-libsonnet/1.23/main.libsonnet";

local k8s_deployment(name, consumer_spec) =
  local deployment = k8s.apps.v1.deployment.new(name=name, containers=[
    k8s.core.v1.container.new(name="consumer", image=p.consumer_image.repo_prefix + name) +
        k8s.core.v1.container.withEnvMap({
            'KAFKA_BOOTSTRAP_SERVER': "aaa"
        } + (if std.objectHas(consumer_spec, 'env') then consumer_spec.env else {}) ) + k8s.core.v1.container.withImagePullPolicy("Never")
  ]);
  deployment + k8s.apps.v1.deployment.metadata.withNamespace("mindwm-consumer");


{
  [consumer_name + "/deployment"]: k8s_deployment(consumer_name, p.mindwm.consumers[consumer_name]) for consumer_name in std.objectFieldsAll(p.mindwm.consumers)
}


