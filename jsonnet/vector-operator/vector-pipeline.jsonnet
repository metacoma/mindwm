local kap = import "lib/kapitan.libjsonnet";
local inventory = kap.inventory();
local p = inventory.parameters;

local vectorPipeline(pipelineName, pipeline) = 
  {
    "apiVersion": "observability.kaasops.io/v1alpha1",
    "kind": "VectorPipeline",
    "metadata": {
       "name": pipelineName,
    },
    "spec": pipeline
  }; 

{
  [pipeline_name]: vectorPipeline(pipeline_name, p.vector.pipeline[pipeline_name]) for pipeline_name in std.objectFieldsAll(p.vector.pipeline)
}

