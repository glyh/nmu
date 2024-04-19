from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

# https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init
class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass

class QuitableServer(ThreadingMixIn, SimpleXMLRPCServer):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.quit = False

    def serve_til_quit(self):
        while not self.quit:
            self.handle_request()

class QuitableService: 
    def __init__(self, server: QuitableServer) -> None:
        self.server = server

    def close_server(self) -> bool:
        if self.server != None:
            self.server.quit = True
        print("exiting")
        return True
