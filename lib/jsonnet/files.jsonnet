local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  [file.path]: kap.jinja2_template("templates/file", {
        data: file.body
  }) for file in p.files
}

