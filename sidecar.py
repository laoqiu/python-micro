#!/usr/bin/env python3
import requests
import json

class Proxy(object):
    def __init__(self, address="127.0.0.1:8081"):
        self.uri = "http://{}".format(address)
        self.headers = {'content-type': 'application/json'}

    def register(self, service):
        return requests.post(self.uri + '/registry', data=json.dumps(service), headers=self.headers)

    def deregister(self, service):
        return requests.delete(self.uri + '/registry', data=json.dumps(service), headers=self.headers)

    def rpc_call(self, path, request):
        return requests.post(self.uri + path, data=json.dumps(request), headers=self.headers).json()

    def http_call(self, path, request):
        return requests.post(self.uri + path, data=request)
