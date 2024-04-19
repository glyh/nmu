from qrterm import qrterm
from textual.widget import Widget

from textual.app import RenderResult

class QRCode(Widget):
    """Display a QRCode."""

    def __init__(self, url, *args) -> None:
        super().__init__(*args)
        self.url = url

    def render(self) -> RenderResult:
        return qrterm.qr_terminal_str(self.url)
