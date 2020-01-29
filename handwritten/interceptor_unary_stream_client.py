from __future__ import print_function

import random
import logging

import grpc
import sys

import echo_pb2
import echo_pb2_grpc
import client_interceptor

def expand(stub):
    responses = stub.Expand(echo_pb2.EchoRequest(content="hello world ! welcome !"))
    for res in responses:
        print(res)
    print("trailing metadata is:")
    print(responses.trailing_metadata())

def run_should_pass():
    header_adder_interceptor = client_interceptor.header_adder_interceptor(
        'one-time-password', '42')
    with grpc.insecure_channel('localhost:50051') as channel:
        intercept_channel = grpc.intercept_channel(channel,
                                                   header_adder_interceptor)
        stub = echo_pb2_grpc.EchoStub(intercept_channel)
        print("================= should pass ====================")
        expand(stub)

def run_should_fail():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = echo_pb2_grpc.EchoStub(channel)
        print("================= should fail with 'Access denied!' ====================")
        try:
            expand(stub)
        except:
            print(sys.exc_info())

if __name__ == '__main__':
    logging.basicConfig()
    run_should_pass()
    run_should_fail()
