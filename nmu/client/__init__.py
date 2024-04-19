import xmlrpc.client as rpcclient
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, ListItem, ListView
import atexit

from nmu.config import Config
from nmu.server.base import QuitableService
from nmu.server.service import NeteaseService

async def get_login_uuid_address() -> str:
    # remote = config.address
    return ""

class ListViewExample(App):

    BINDINGS = [
        ("a", "addone", "Add"),
        ("l", "login", "Login"),
    ]

    def __init__(self, service: NeteaseService, *args) -> None:
        super().__init__(*args)
        self.service = service

    async def init_login(self) -> None:
        music_list: ListView = self.query_one('#music_list')
        # label = str(self.service.get_answer())
        # music_list.append(ListItem(Label(label)))
        music_list.append(ListItem(Label("hey")))

    def on_mount(self) -> None:
        pass
        # self.run_worker(self.init_login())

    def compose(self) -> ComposeResult:
        yield ListView(id='music_list')
        yield Footer()

    def action_login(self) -> None:
        """Login."""
        music_list: ListView = self.query_one('#music_list')
        music_list.append(ListItem(Label("hehe")))

    def action_addone(self) -> None:
        """Add one `hehe`."""
        music_list: ListView = self.query_one('#music_list')
        music_list.append(ListItem(Label("hehe")))

def run():
    config = Config()
    service: QuitableService = rpcclient.ServerProxy(f"http://{config.server_address}:{config.server_port}/")

    def exit_handler():
        print(service.close_server())

    atexit.register(exit_handler)

    app = ListViewExample(service)
    app.run()
