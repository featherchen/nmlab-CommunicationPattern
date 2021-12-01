from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from google.protobuf.json_format import MessageToJson, MessageToDict

# Create your views here.
class EchoView1(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'fibonacci' }, status=200)

class EchoView2(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'logs' }, status=200)

class Fibonacci(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        import os
        import os.path as osp
        import sys
        # BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
        # sys.path.insert(0, BUILD_DIR)
        GRPC_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC-with-protobuf/build/service/")
        sys.path.insert(0, GRPC_DIR)
        import argparse

        import grpc
        import fib_pb2
        import fib_pb2_grpc

        order=int(request.data["order"])
        # host = f"{args['ip']}:{args['port']}"
        # print(host)
        host = "localhost:8080"
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            req = fib_pb2.FibRequest()
            req.order = order

            response = stub.Compute(req)
            # print(response.value)

        return Response(data={ 'echo': response.value }, status=200)


class Logging(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        import os
        import os.path as osp
        import sys
        # BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
        # sys.path.insert(0, BUILD_DIR)
        GRPC_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC-with-protobuf/build/service/")
        sys.path.insert(0, GRPC_DIR)
        import argparse

        import grpc
        import fib_pb2
        import fib_pb2_grpc

        # order=int(request.data["order"])
        # host = f"{args['ip']}:{args['port']}"
        # print(host)
        host = "localhost:8080"
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.LoggerCalculatorStub(channel)

            req = fib_pb2.LogRequest()
            # req.order = order

            response = stub.Log(req)
            # print(response.value)
            # print(response)
            # serialized = MessageToJson(response)
            response = MessageToDict(response, preserving_proto_field_name = True)
            desired_res = response["history"]
            history=[int(i) for i in desired_res]
        return Response(data={ 'echo': history }, status=200)
