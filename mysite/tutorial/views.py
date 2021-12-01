from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from google.protobuf.json_format import MessageToJson, MessageToDict

import time
import argparse

import psutil
import paho.mqtt.client as mqtt

# import threading
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
        # BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
        # sys.path.insert(0, BUILD_DIR)
        GRPC_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC-with-protobuf/build/service/")
        sys.path.insert(0, GRPC_DIR)
        import argparse

        import grpc
        import fib_pb2
        import fib_pb2_grpc

        order=int(request.data["order"])
        self.client.publish(topic="LOG", payload=order)
        # host = f"{args['ip']}:{args['port']}"
        # print(host)
        host = "localhost:8080"
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            req = fib_pb2.FibRequest()
            req.order = order

            response = stub.Compute(req)
            # print(response.value)

        return Response(data={ 'Fibonacci': response.value }, status=200)


# def on_message(client, obj, msg):
#     global History
#     # print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
#     # print(msg.payload)
#     History=msg.payload
#     # print("XXXX")
#     client.disconnect()

# def job():
#     client = mqtt.Client()
#     client.on_message = on_message
#     client.connect(host="localhost", port=1883)
#     client.subscribe('LOG', 0)
#     # client.subscribe('mem', 0)
#     try:
#         client.loop_forever()
#     except KeyboardInterrupt as e:
#         pass    
class Logging(APIView):
    permission_classes = (permissions.AllowAny,)
    history=[]

    def __init__(self):
        pass
        # self.on_message=on_message(client, obj, msg):

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


        # client = mqtt.Client()
        # client.on_message = on_message
        # client.connect(host="localhost", port=1883)
        # client.subscribe('LOG', 0)
        # # client.subscribe('mem', 0)
        # try:
        #     client.loop_forever()
        # except KeyboardInterrupt as e:
        #     pass    
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
        # return Response(data={ 'echo': history }, status=200)
        return Response(data={ 'history': history }, status=200)
