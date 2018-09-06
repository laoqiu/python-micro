import inspect
from jsonrpc import dispatcher

def addMethod(cls):
    for name, func in inspect.getmembers(cls):
        if not name.startswith("_"):
            print(cls.__name__, name)
            dispatcher.add_method(func, name="%s.%s" % (cls.__name__, name))