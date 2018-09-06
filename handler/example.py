from .base import addMethod

@addMethod
class Example(object):
    @staticmethod
    def Call(request):
        return dict(msg="test")