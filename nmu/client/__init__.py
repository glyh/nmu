from typing import Any
import xmlrpc.client as rpcclient
from textual.app import App, ComposeResult
from textual.widgets import Footer, Input, Label, ListItem, ListView
import atexit

from nmu.config import Config
from nmu.server.service import NeteaseService

from .widgets import QRCode

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
        self.need_verrify = False

    async def init_login_qr(self) -> None:
        music_list: ListView = self.query_one('#music_list')
        label = str(self.service.get_answer())
        music_list.append(ListItem(Label(label)))
        login_addr = self.service.get_login_url()
        music_list.append(ListItem(QRCode(login_addr)))

    async def init_login(self) -> None:
        l: ListView = self.query_one('#music_list')
        resp: dict[str, Any] = self.service.get_captcha_via_phone('13166107672', '86')
        l.append(ListItem(Label(str(resp))))
        if resp.get('code', 0) == 200:
            self.need_verrify = True
            self.phone = '13166107672'
            self.ctcode = '86'
            
        # result = SetSendRegisterVerifcationCodeViaCellphone(phone,ctcode)        
        # if not result.get('code',0) == 200:
        #     pprint(result)
        # else:
        #     print('[-] 已发送验证码')    
        # while True:
        #     captcha = inquirer.text("输入验证码")
        #     verified = GetRegisterVerifcationStatusViaCellphone(phone,captcha,ctcode)
        #     pprint(verified)
        #     if verified.get('code',0) == 200:
        #         print('[-] 验证成功')
        #         break
        # result = LoginViaCellphone(phone,captcha=captcha,ctcode=ctcode)
        # pprint(result)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        l: ListView = self.query_one('#music_list')
        if event.input.id == 'captcha' and self.need_verrify:
            verified: dict[str, Any] = self.service.verify_captcha_via_phone(self.phone, event.input.value ,self.ctcode)
            l.append(ListItem(Label(str(verified))))
            if verified.get('code',0) == 200:
                out = self.service.login_via_phone(self.phone, event.input.value ,self.ctcode)
                l.append(ListItem(Label(str(out))))

    def compose(self) -> ComposeResult:
        yield ListView(id='music_list')
        yield Input(id='captcha')
        yield Footer()

    async def action_login(self) -> None:
        """Login."""
        await self.init_login()

    def action_addone(self) -> None:
        """Add one `hehe`."""
        music_list: ListView = self.query_one('#music_list')
        music_list.append(ListItem(Label("hehe")))




def run():
    config = Config()
    service: NeteaseService = rpcclient.ServerProxy(f"http://{config.server_address}:{config.server_port}/")

    def exit_handler():
        print(service.close_server())

    atexit.register(exit_handler)

    app = ListViewExample(service)
    app.run()
