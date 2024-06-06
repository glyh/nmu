import time
from typing import Any
from pyncm import Session, apis
import pyncm

from nmu.server.base import QuitableService

class NeteaseService(QuitableService):
    def __init__(self, *args):
        super().__init__(*args)
        self.session: Session = pyncm.CreateNewSession()
        response: dict[str, Any] = apis.login.LoginQrcodeUnikey()
        self.uuid: str = response["unikey"]

    def get_answer(self) -> int:
        return 42

    def get_login_url(self) -> str:
        return f"https://music.163.com/login?codekey={self.uuid}"

    # TODO: deal with failing case
    def wait_login(self) -> dict[str, Any]:
        while True:
            rsp: dict[str, Any] = apis.login.LoginQrcodeCheck(self.uuid)  # 检测扫描状态
            if rsp["code"] == 803 or rsp["code"] == 800:
                status = apis.login.GetCurrentLoginStatus()
                apis.login.WriteLoginInfo(status, self.session)
                return status
            time.sleep(1)

    def get_captcha_via_phone(self, phone, ctcode):
        return apis.login.SetSendRegisterVerifcationCodeViaCellphone(phone, ctcode)

    def verify_captcha_via_phone(self, phone, captcha, ctcode):
        verified = apis.login.GetRegisterVerifcationStatusViaCellphone(phone,captcha,ctcode)
        return verified

    def login_via_phone(self, phone, captcha, ctcode):
        verified = apis.login.LoginViaCellphone(phone,captcha,ctcode)
        return verified
        

