from typing import Union, Any

from .config import EmailURL
from .message import EmailMessage
from .transports import create_transport, BaseTransport


class Mailer:
    def __init__(self, url_or_transport: Union[str, EmailURL, BaseTransport]):
        if isinstance(url_or_transport, BaseTransport):
            self._transport = url_or_transport
        else:
            self._transport = create_transport(url_or_transport)

    async def send(self, message: EmailMessage) -> Any:
        return await self._transport.send(message)
