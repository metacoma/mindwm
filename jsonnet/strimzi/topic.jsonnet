local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;
local strimzi = import "files/github.com/jsonnet-libs/strimzi-libjsonnet/0.32/main.libsonnet";

local kafkaTopic = strimzi.kafka.v1beta2.kafkaTopic;

local kafkaTopicResource(spec) = 
  local newKafkaTopic = kafkaTopic.new(
    name = spec.name,
  ); 
  local kafkaTopicConfig = kafkaTopic.spec.withConfig(spec.config);
  newKafkaTopic + 
    kafkaTopic.metadata.withLabels({
       "strimzi.io/cluster": p.kafka_cluster_name
    }) +
    kafkaTopic.spec.withReplicas(std.get(spec, "replicas", default=1)) +
    kafkaTopic.spec.withPartitions(std.get(spec, "partitions", default=1)) + 
    kafkaTopicConfig;
  


{
  [kafka_topic]: kafkaTopicResource(p.kafka_topics[kafka_topic]) for kafka_topic in std.objectFieldsAll(p.kafka_topics)

}
