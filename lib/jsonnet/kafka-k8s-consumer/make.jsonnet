local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  [consumer_name + "/Makefile"]: kap.jinja2_template("templates/kafka/k8s-consumer/Makefile", {
        inventory: inventory,
        consumer: p.kafka.consumers[consumer_name],
        consumer_name: consumer_name
  }) for consumer_name in std.objectFieldsAll(p.kafka.consumers)
}

