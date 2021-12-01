from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from google.protobuf.json_format import MessageToJson, MessageToDict

import time
import argparse

import psutil
import paho.mqtt.client as mqtt

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

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(host="localhost", port=1883)
        self.client.loop_start()
        pass

    def post(self, request):
        import os
        import os.path as osp
        import sys

        GRPC_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC-with-protobuf/build/service/")
        sys.path.insert(0, GRPC_DIR)
        import argparse

        import grpc
        import fib_pb2
        import fib_pb2_grpc

        order=int(request.data["order"])
        self.client.publish(topic="LOG", payload=order)

        host = "localhost:8080"
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            req = fib_pb2.FibRequest()
            req.order = order

            response = stub.Compute(req)

        return Response(data={ 'Fibonacci': response.value }, status=200)

class Logging(APIView):
    permission_classes = (permissions.AllowAny,)
    history=[]

    def __init__(self):
        pass

    def get(self, request):
        import os
        import os.path as osp
        import sys
 
        GRPC_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC-with-protobuf/build/service/")
        sys.path.insert(0, GRPC_DIR)
        import argparse

        import grpc
        import fib_pb2
        import fib_pb2_grpc

        host = "localhost:8080"
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.LoggerCalculatorStub(channel)

            req = fib_pb2.LogRequest()
            response = stub.Log(req)

            response = MessageToDict(response, preserving_proto_field_name = True)
            if "history" in response:
                desired_res = response["history"]
            else:
                desired_res=[] 
            history=[int(i) for i in desired_res]
        return Response(data={ 'history': history }, status=200)
