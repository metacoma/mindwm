from __future__ import print_function

import logging

import grpc
import freeplane_pb2
import freeplane_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051') 
    fp = freeplane_pb2_grpc.FreeplaneStub(channel)
    response = fp.CreateChild(freeplane_pb2.CreateChildRequest(name='testPython', parent_node_id = ""))
    print("Greeter client received: " + response.node_id)


if __name__ == '__main__':
    logging.basicConfig()
    run()

