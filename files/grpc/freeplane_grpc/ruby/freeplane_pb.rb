# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: freeplane.protoc

require 'google/protobuf'

Google::Protobuf::DescriptorPool.generated_pool.build do
  add_file("freeplane.protoc", :syntax => :proto3) do
    add_message "freeplane.createChildRequest" do
      optional :name, :string, 1
    end
    add_message "freeplane.createChildResponse" do
      optional :message, :string, 1
    end
  end
end

module Freeplane
  CreateChildRequest = ::Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.createChildRequest").msgclass
  CreateChildResponse = ::Google::Protobuf::DescriptorPool.generated_pool.lookup("freeplane.createChildResponse").msgclass
end
