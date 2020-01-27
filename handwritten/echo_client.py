from __future__ import print_function

import random
import logging

import grpc

import echo_pb2
import echo_pb2_grpc


def echo(stub):
    request = echo_pb2.EchoRequest(content="hello world!")
    return stub.Echo(request)

def expand(stub):
    responses = stub.Expand(echo_pb2.EchoRequest(content="hello world ! welcome !"))
    for res in responses:
        print(res)

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
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = echo_pb2_grpc.EchoStub(channel)
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