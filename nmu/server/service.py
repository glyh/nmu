import asyncio
from typing import Any, Awaitable
from pyncm_async import Session, apis
import pyncm_async

from nmu.server.base import QuitableServer, QuitableService, aobject

class NeteaseService(QuitableService, aobject):
    async def __init__(self, *args):
        super().__init__(*args)
        self.session: Session = pyncm_async.CreateNewSession()
        response = await apis.login.LoginQrcodeUnikey()
        self.uuid: str = response["unikey"]
        return self

    def get_answer(self) -> int:
        return 42

    def get_login_url(self) -> str:
        return f"https://music.163.com/login?codekey={self.uuid}"

    # TODO: deal with failing case
    async def wait_login(self) -> dict[str, Any]:
        while True:
            rsp: dict[str, Any] = await apis.login.LoginQrcodeCheck(self.uuid)  # 检测扫描状态
            if rsp["code"] == 803 or rsp["code"] == 800:
                status = await apis.login.GetCurrentLoginStatus()
                apis.login.WriteLoginInfo(status, self.session)
                return status
            await asyncio.sleep(1)
