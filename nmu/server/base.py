from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

class QuitableServer(ThreadingMixIn, SimpleXMLRPCServer):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
