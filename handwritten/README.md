# 1. Run client and server

This client and server implement the services in echo.proto in gapic-showcase.

```
python server.py
```
```
python client.py
```

# 2. Run stream-stream/unary-stream server and client with intercetpors
Server has an interceptor which checks the existences of a ('one-time-password', '42') header and aborts if not. Client has two methods, "run_should_pass" which implements an interceptor adding the header, and "run_should_fail" which doesn't.

For stream-stream
```
python interceptor_stream_stream_server.py
```
```
python interceptor_stream_stream_client.py
```

For unary-stream
```
python interceptor_unary_stream_server.py
```
```
python interceptor_unary_stream_client.py
```
