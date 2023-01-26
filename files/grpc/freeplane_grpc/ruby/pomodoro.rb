#!/usr/bin/env ruby

# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Sample app that connects to a Greeter service.
#
# Usage: $ path/to/greeter_client.rb

this_dir = File.expand_path(File.dirname(__FILE__))
lib_dir = File.join(this_dir, 'lib')
$LOAD_PATH.unshift(lib_dir) unless $LOAD_PATH.include?(lib_dir)

require 'json'
require 'time'
require 'grpc'
require 'freeplane_services_pb'

def pomo_time(t)
  return Time.parse(t).strftime "%H:%M"
end


def main
  pomo_data =  JSON.parse(ARGF.read)
  stub = Freeplane::Freeplane::Stub.new('localhost:50051', :this_channel_is_insecure)
  pomodoro = stub.create_child(Freeplane::CreateChildRequest.new(name: "pomodoro", parent_node_id: ""))
  stub.node_attribute_add(Freeplane::NodeAttributeAddRequest.new(node_id: pomodoro["node_id"], attribute_name: pomo_time(pomo_data["start"]), attribute_value: pomo_time(pomo_data["end"])))


  session_n = 1
  pomo_index = 1

  pomo_session = stub.create_child(Freeplane::CreateChildRequest.new(name: "session#{session_n}", parent_node_id: pomodoro["node_id"]))

  for segment in pomo_data['segments'] do
    if (segment["type"] == "pomodoro") then
      segment_node = stub.create_child(Freeplane::CreateChildRequest.new(name: "pomodoro#{pomo_index}", parent_node_id: pomo_session["node_id"]))
      stub.node_attribute_add(Freeplane::NodeAttributeAddRequest.new(node_id: segment_node["node_id"], attribute_name: pomo_time(segment["start"]), attribute_value: pomo_time(segment["end"])))
      pomo_index = pomo_index + 1

      stub.node_background_color_set(Freeplane::NodeBackgroundColorSetRequest.new(node_id: segment_node["node_id"], red: 255, green: 120, blue: 120, alpha: 255))
    end
    if (segment["type"] == "long-break") then
      pomo_inde = 1
      session_n = session_n + 1
      pomo_session = stub.create_child(Freeplane::CreateChildRequest.new(name: "session#{session_n}", parent_node_id: pomodoro["node_id"]))
    end
  end
    
  

  # create pomodoro mindmap node as child for the root node 
#  pomodoro = stub.create_child(Freeplane::CreateChildRequest.new(name: "pomodoro", parent_node_id: ""))
#  session1 = stub.create_child(Freeplane::CreateChildRequest.new(name: "session1", parent_node_id: pomodoro["node_id"]))
#  session2 = stub.create_child(Freeplane::CreateChildRequest.new(name: "session2", parent_node_id: pomodoro["node_id"]))
#  session3 = stub.create_child(Freeplane::CreateChildRequest.new(name: "session3", parent_node_id: pomodoro["node_id"]))
#  session4 = stub.create_child(Freeplane::CreateChildRequest.new(name: "session4", parent_node_id: pomodoro["node_id"]))
#
#  pomo1 = stub.create_child(Freeplane::CreateChildRequest.new(name: "pomo1", parent_node_id: session1["node_id"]))
#  pomo2 = stub.create_child(Freeplane::CreateChildRequest.new(name: "pomo2", parent_node_id: session1["node_id"]))
#  pomo3 = stub.create_child(Freeplane::CreateChildRequest.new(name: "pomo3", parent_node_id: session1["node_id"]))
#  pomo4 = stub.create_child(Freeplane::CreateChildRequest.new(name: "pomo4", parent_node_id: session1["node_id"]))
#
#  stub.node_color_set(Freeplane::NodeColorSetRequest.new(node_id: pomo1["node_id"], red: 255, green: 255, blue: 255, alpha: 0))
#  stub.node_background_color_set(Freeplane::NodeBackgroundColorSetRequest.new(node_id: pomo1["node_id"], red: 0, green: 255, blue: 0, alpha: 0))
  

end

main
