#!/usr/bin/env bash

# https://docs.fluentbit.io/manual/pipeline/inputs/tail
# i don't why, but fluent-bit accepts only json in stdin plugin
# https://github.com/fluent/fluent-bit/blob/2a4d62b38b5c1c997f6e67660aeb8b11dddab5f9/plugins/in_stdin/in_stdin.c

export NODE_ID=test_node_id
echo hello world | fluent-bit --verbose  --input stdin --parser ./parser.conf -o stdout 
#echo '{"name": "bob"}' | fluent-bit --verbose  --input stdin --parser ./parser.conf -o stdout 

