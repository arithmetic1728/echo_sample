from __future__ import print_function

import random
import logging

import grpc

import echo_pb2
import echo_pb2_grpc
import header_manipulator_client_interceptor


def echo(stub):
    request = echo_pb2.EchoRequest(content="hello world!")
    response = stub.Echo(request)
    print(response)

def expand(stub):
    responses = stub.Expand(echo_pb2.EchoRequest(content="hello world ! welcome !"))
    for res in responses:
        print(res)
    print("trailing metadata is:")
    print(responses.trailing_metadata())

def collect(stub):
    mylist = []
    mylist.append(echo_pb2.EchoRequest(content="hello"))
    mylist.append(echo_pb2.EchoRequest(content="world"))
    mylist.append(echo_pb2.EchoRequest(content="!"))
    response = stub.Collect(iter(mylist))
    print(response)


def chat(stub):
    mylist = []
    mylist.append(echo_pb2.EchoRequest(content="hello"))
    mylist.append(echo_pb2.EchoRequest(content="world"))
    mylist.append(echo_pb2.EchoRequest(content="!"))
    responses = stub.Chat(iter(mylist), metadata=(
                ('initial-metadata-1', 'The value should be str'),
                ('binary-metadata-bin',
                 b'With -bin surffix, the value can be bytes'),
                ('accesstoken', 'gRPC Python is great'),
            ))
    for response in responses:
        print(response)
    print("trailing metadata is:")
    print(responses.trailing_metadata())


def run():
    header_adder_interceptor = header_manipulator_client_interceptor.header_adder_interceptor(
        'one-time-password', '42')
    with grpc.insecure_channel('localhost:50051') as channel:
        intercept_channel = grpc.intercept_channel(channel,
                                                   header_adder_interceptor)
        stub = echo_pb2_grpc.EchoStub(intercept_channel)
        print("-------------- Echo --------------")
        echo(stub)
        print("-------------- Expand --------------")
        expand(stub)
        print("-------------- Collect --------------")
        collect(stub)
        print("-------------- Chat --------------")
        chat(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
