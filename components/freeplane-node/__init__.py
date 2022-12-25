# components/tinyapp/__init__.py
from kapitan.inputs.kadet import BaseOBj, inventory
inv = inventory() # returns inventory for target being compiled

class TinyApp(BaseObj):
  def body(self):
    self.root.foo = "bar"
    self.root.replicas = inv.parameters.tinyapp.replicas

def main():
  obj = BaseOb()
  obj.root.deployment = TinyApp() # will compile into deployment.yml
  return obj
