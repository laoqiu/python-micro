import sys
import json
import uuid
import logging
import signal
import getopt
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from jsonrpc import JSONRPCResponseManager, dispatcher
from handler import example
from sidecar import Proxy

logging.basicConfig(level=logging.DEBUG)

def get_service(name, host, port):
    return {
        "name": name,
        "nodes": [{
            "id": "%s-%s" % (name, uuid.uuid4().hex),
            "host": host,
            "port": port,
        }],
    }

class MainHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        logging.info(self.headers)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        response = JSONRPCResponseManager.handle(body, dispatcher)
        self.write(response.json)

    def write(self, msg):
        self.send_response(200)
        self.send_header("Content-Type", 'application/json; charset=utf-8')
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg.encode('UTF-8'))


def usage():
    """
    Usage: main.py [-h|--help] [--host,127.0.0.1] [-p|--port,5000] [--proxy,127.0.0.1:8081]
    """

def main(args):
    options = dict(
        name="go.micro.srv.greeter",
        host="127.0.0.1",
        port=5000,
        proxy="127.0.0.1:8081"
    )
    if args:
        for k, v in getopt.getopt(args, 'hp:n:', ["help", "host=", "port=", "name=", "proxy="])[0]:
            if k in ("-h", "--help"):
                print(usage.__doc__)
                sys.exit(0)
            elif k in ("-n", "--name"):
                options['name'] = v
            elif k in ("-p", "--port"):
                options['port'] = int(v)
            elif k in ("--host", ):
                options['host'] = v
            elif k in ("--proxy",):
                options['proxy'] = v
            else:
                print("Using the wrong way,please view the help information.")
                sys.exit(0)

    # register consul service
    service = get_service(options['name'], options['host'], options['port'])
    proxy = Proxy()
    proxy.register(service)

    # server start
    httpd = ThreadingHTTPServer((options['host'], options['port']), MainHandler)

    def stop_handler(signum, frame):  
        logging.info("service {} stop".format(options['name']))
        proxy.deregister(service)
        httpd.server_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)

    logging.info("service [{}] start at [{}]".format(options['host'], options['port']))
    httpd.serve_forever()

if __name__ == '__main__':
    main(sys.argv[1:])