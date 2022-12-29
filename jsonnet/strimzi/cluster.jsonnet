local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;
// https://github.com/google/go-jsonnet/blob/f699b0ea4251b6c63b7b9860b5a6e9c68a4f4aef/internal/parser/parser.go#L1091 
// why?
local strimzi = import "files/github.com/jsonnet-libs/strimzi-libjsonnet/0.32/main.libsonnet";

local kafka = strimzi.kafka.v1beta2.kafka;

local kafkaResource(clusterName, spec) = 
  local newKafka = kafka.new(clusterName);
  newKafka + {
    "spec": spec
  } + kafka.spec.kafka.withReplicas(std.get(spec.kafka, "replicas", 1));

{
  [cluster_name]: kafkaResource(cluster_name, p.kafka_clusters[cluster_name]) for cluster_name in std.objectFieldsAll(p.kafka_clusters)
}
