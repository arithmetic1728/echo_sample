from concurrent import futures
import time
import math
import logging

import grpc

import echo_pb2
import echo_pb2_grpc

def _unary_stream_rpc_terminator(code, details):

    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_stream_rpc_method_handler(terminate)


class RequestHeaderValidatorInterceptor(grpc.ServerInterceptor):

    def __init__(self, header, value, code, details):
        self._header = header
        self._value = value
        self._terminator = _unary_stream_rpc_terminator(code, details)

    def intercept_service(self, continuation, handler_call_details):
        if (self._header,
                self._value) in handler_call_details.invocation_metadata:
            print("-----interceptor is called, continue-----")
            return continuation(handler_call_details)
        else:
            print("-----interceptor is called, terminating-----")
            return self._terminator

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
        context.set_trailing_metadata((
            ('checksum-bin', b'I agree'),
            ('retry', 'false'),
        ))
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
    header_validator = RequestHeaderValidatorInterceptor(
        'one-time-password', '42', grpc.StatusCode.UNAUTHENTICATED,
        'Access denied!')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=(header_validator,))
    echo_pb2_grpc.add_EchoServicer_to_server(
        EchoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
