local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  [consumer_name + "/consumer"]: kap.jinja2_template("templates/mindwm/consumer/consumer", {
        inventory: inventory,
        consumer: p.mindwm.consumers[consumer_name]
  }) for consumer_name in std.objectFieldsAll(p.mindwm.consumers)
}

