from multiprocessing import Process
import nmu.client as client
import nmu.server as server
from nmu.server.service import NeteaseService

def sync_entry():
    Process(target=server.run_sync).start()
    client.run()

if __name__ == "__main__":
    sync_entry()
