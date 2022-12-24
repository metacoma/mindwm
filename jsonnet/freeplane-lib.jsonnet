local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  [lib_name + ".groovy"]: kap.jinja2_template("templates/freeplane/lib/FP.groovy", {
        groovy_code: p.freeplane.lib[lib_name]
  }) for lib_name in std.objectFieldsAll(p.freeplane.lib)
/*
  [lib_name]: kap.jinja2_template("templates/freeplane/lib/FP.groovy", {
        groovy_code: "xxxx"
  }) for lib_name in in std.objectFieldsAll(p.freeplane.lib)
*/
}

