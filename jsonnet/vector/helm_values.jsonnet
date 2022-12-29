local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

{
  values: p.vector.aggregator
  /*
  "values": {
    "image": {
      "repository": p.vector_image.repo,
      "tag": p.vector_image.tag,
    }, 
    "customConfig": p.vector.aggregator.config,
  } + (if 'service' in p.vector.aggregator then p.vector.aggregator else {})
  */
  
}

