from __future__ import print_function

import logging

import grpc
import freeplane_pb2
import freeplane_pb2_grpc
import sys
import json

def run():
    ec2_list_data = json.load(sys.stdin)

    channel = grpc.insecure_channel('localhost:50051') 
    fp = freeplane_pb2_grpc.FreeplaneStub(channel)

    ec2_node = fp.CreateChild(freeplane_pb2.CreateChildRequest(name='ec2', parent_node_id = ""))

    for ec2_instance in ec2_list_data["Instances"]:
      instance_node = fp.CreateChild(freeplane_pb2.CreateChildRequest(name=ec2_instance["Ec2InstanceId"], parent_node_id = ec2_node.node_id))
      fp.NodeAttributeAdd(freeplane_pb2.NodeAttributeAddRequest(node_id=instance_node.node_id, attribute_name="Public", attribute_value=ec2_instance['PublicIpAddress'])) 
      fp.NodeAttributeAdd(freeplane_pb2.NodeAttributeAddRequest(node_id=instance_node.node_id, attribute_name="Private", attribute_value=ec2_instance['PrivateIpAddress'])) 
      if ec2_instance['Status']['State'] != "RUNNING": 
        fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id=instance_node.node_id, red=255, green=120, blue=120, alpha=255)) 
      else:
        fp.NodeBackgroundColorSet(freeplane_pb2.NodeBackgroundColorSetRequest(node_id=instance_node.node_id, red=120, green=200, blue=120, alpha=255)) 

      fp.NodeDetailsSet(freeplane_pb2.NodeDetailsSetRequest(node_id=instance_node.node_id, details=ec2_instance['PublicDnsName']))
      fp.NodeLinkSet(freeplane_pb2.NodeLinkSetRequest(node_id=instance_node.node_id, link='execute:_xterm -e ssh ' + ec2_instance['PublicIpAddress']))

if __name__ == '__main__':
    logging.basicConfig()
    run()

