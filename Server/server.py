#! /usr/bin/env python
# -*- coding: utf-8 -*-

from example import LockService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from example.ttypes import Response

__HOST = 'localhost'
__PORT = 8080
resources = {"A", "B", "C", "D", "E"} #Assuming we have 5 resources
lock_dict = {}  #store processes which have lock(s) and what lock they have
lock_set = set()   #store locked resources


class LockServiceHandler(object):
    def acquire_lock(self, request):
        if request.resource not in lock_set and request.resource in resources:
            if request.pid in lock_dict.keys():
                lock_dict[request.pid].append(request.resource)
            else:
                lock_dict[request.pid] = [request.resource]
            lock_set.add(request.resource)
            response = Response(pid=request.pid, resource=request.resource, operation="success")
        else:
            response = Response(pid=request.pid, resource=request.resource, operation="fail")
        return response

    def release_lock(self, request):
        if request.resource in lock_set:
            lock_dict[request.pid].pop(lock_dict[request.pid].index(request.resource))
            lock_set.remove(request.resource)
            response = Response(pid=request.pid, resource=request.resource, operation="success")
        else:
            response = Response(pid=request.pid, resource=request.resource, operation="fail")
        return response


if __name__ == '__main__':

    handler = LockServiceHandler()
    processor = LockService.Processor(handler)
    transport = TSocket.TServerSocket(__HOST, __PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    rpcServer = TServer.TSimpleServer(processor,transport, tfactory, pfactory)

    print('Starting the rpc server at', __HOST,':', __PORT)
    rpcServer.serve()
    print("done!")

