local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;


{
	[processing_name + "/requirements.txt"]: kap.jinja2_template("templates/neomodel/requirements.txt", {
		inventory: inventory,
		processing: p.mindwm2[processing_name]
	}) for processing_name in std.objectFields(p.mindwm2)
}
