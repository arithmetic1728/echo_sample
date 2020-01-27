```
python -m grpc_tools.protoc -I./protos/google/showcase/v1beta1 -
I./protos/api-common-protos --python_out=. --grpc_python_out=. protos/google/showcase/v1beta1/*.proto
```
