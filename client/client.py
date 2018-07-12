#! /usr/bin/env python
# -*- coding: utf-8 -*-

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift import Thrift
from example.ttypes import Response
from example.ttypes import Request
from example.LockService import Client






__HOST = 'localhost'
__PORT = 8080

tsocket = TSocket.TSocket(__HOST, __PORT)
transport = TTransport.TBufferedTransport(tsocket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Client(protocol)
transport.open()
try:
    while True:
        print("Please input command like this:")
        print("processId lock/unlock resource")
        print("enter \"exit\" to exit")
        command = input().split()
        if command[0] == "exit":
            break
        if len(command) is not 3:
            print("command arguments number must be 3!\n")
            continue
        if command[1] not in ["lock", "unlock"]:
            print("second command argument  must be lock or unlock!\n")
        request = Request(pid=int(command[0]), operation=command[1], resource=command[2])
        if command[1] == "lock":
            response = client.acquire_lock(request)
            if response.operation == "success":
                print("Process %d acquire resource %s lock successfully." %(response.pid, response.resource))
            if response.operation == "fail":
                print("Process %d acquire resource %s lock failed." %(response.pid, response.resource))
        if command[1] == "unlock":
            response = client.release_lock(request)
            if response.operation == "success":
                print("Process %d release resource %s lock successfully." % (response.pid, response.resource))
            if response.operation == "fail":
                print("Process %d release resource %s lock failed." % (response.pid, response.resource))

    transport.close()

except Thrift.TException as ex:
    print("%s" % (ex.message))