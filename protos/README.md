1. How to compile the gapic-showcase protos.

The gapic-showcase protos are in /google/ folder.

```
python -m grpc_tools.protoc -I./google/showcase/v1beta1 \
 -I./api-common-protos --python_out=./generated \
 --grpc_python_out=./generated google/showcase/v1beta1/*.proto
```
