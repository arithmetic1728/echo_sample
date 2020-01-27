from concurrent import futures
import time
import math
import logging

import grpc

import echo_pb2
import echo_pb2_grpc

class EchoServicer(echo_pb2_grpc.EchoServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        pass

    def Echo(self, request, context):
        print("==== received request for Echo ===")
        print(request)
        return echo_pb2.EchoResponse(content=request.content)

    def Expand(self, request, context):
        print("==== received request for Expand ===")
        print(request)
        arr = request.content.split()
        for word in arr:
            yield echo_pb2.EchoResponse(content=word)

    def Collect(self, request_iterator, context):
        print("==== received request for Collect ===")
        res = ""
        for req in request_iterator:
            res = res + " " + req.content
        return echo_pb2.EchoResponse(content=res)

    def Chat(self, request_iterator, context):
        print("==== received request for Chat ===")
        for key, value in context.invocation_metadata():
            print('Received initial metadata: key=%s value=%s' % (key, value))
        context.set_trailing_metadata((
            ('checksum-bin', b'I agree'),
            ('retry', 'false'),
        ))
        for req in request_iterator:
            yield echo_pb2.EchoResponse(content=req.content)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServicer_to_server(
        EchoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()