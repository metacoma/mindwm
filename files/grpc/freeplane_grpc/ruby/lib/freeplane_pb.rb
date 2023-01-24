# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: freeplane.proto

require 'google/protobuf'

Google::Protobuf::DescriptorPool.generated_pool.build do
  add_message "freeplane.CreateChildRequest" do
    optional :name, :string, 1
  end
  add_message "freeplane.CreateChildResponse" do
    optional :node_id, :string, 1
    optional :node_text, :string, 2
  end
  add_message "freeplane.DeleteChildRequest" do
    optional :node_id, :string, 1
  end
  add_message "freeplane.DeleteChildResponse" do
    optional :success, :bool, 1
  end
  add_message "freeplane.NodeAttributeAddRequest" do
    optional :node_id, :string, 1
    optional :property_name, :string, 2
    optional :property_value, :string, 3
  end
  add_message "freeplane.NodeAttributeAddResponse" do
    optional :success, :bool, 1
  end
end

module Freeplane
  CreateChildRequest = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.CreateChildRequest").msgclass
  CreateChildResponse = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.CreateChildResponse").msgclass
  DeleteChildRequest = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.DeleteChildRequest").msgclass
  DeleteChildResponse = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.DeleteChildResponse").msgclass
  NodeAttributeAddRequest = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.NodeAttributeAddRequest").msgclass
  NodeAttributeAddResponse = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.NodeAttributeAddResponse").msgclass
end
