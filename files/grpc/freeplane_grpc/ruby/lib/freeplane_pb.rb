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
    optional :attribute_name, :string, 2
    optional :attribute_value, :string, 3
  end
  add_message "freeplane.NodeAttributeAddResponse" do
    optional :success, :bool, 1
  end
  add_message "freeplane.NodeLinkSetRequest" do
    optional :node_id, :string, 1
    optional :link, :string, 2
  end
  add_message "freeplane.NodeLinkSetResponse" do
    optional :success, :bool, 1
  end
  add_message "freeplane.NodeDetailsSetRequest" do
    optional :node_id, :string, 1
    optional :details, :string, 2
  end
  add_message "freeplane.NodeDetailsSetResponse" do
    optional :success, :bool, 1
  end
  add_message "freeplane.GroovyRequest" do
    optional :groovy_code, :string, 1
  end
  add_message "freeplane.GroovyResponse" do
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
  NodeLinkSetRequest = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.NodeLinkSetRequest").msgclass
  NodeLinkSetResponse = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.NodeLinkSetResponse").msgclass
  NodeDetailsSetRequest = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.NodeDetailsSetRequest").msgclass
  NodeDetailsSetResponse = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.NodeDetailsSetResponse").msgclass
  GroovyRequest = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.GroovyRequest").msgclass
  GroovyResponse = Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.GroovyResponse").msgclass
end
