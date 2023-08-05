"""Configuration via URL.

Based on https://github.com/encode/databases/blob/master/databases/core.py#L323
"""
import typing
from urllib.parse import urlsplit, parse_qsl, ParseResult

SUPPORTED_BACKENDS = {
    'smtp': 'mailables.transports:smtp_transport_factory',
    'file': 'mailables.transports:file_transport_factory',
    'null': 'mailables.transports:null_transport_factory',
    'memory': 'mailables.transports:memory_transport_factory',
}


class EmailURL:
    def __init__(self, url: str):
        self._url = url

    @property
    def components(self):
        if not hasattr(self, '_components'):
            self._components: ParseResult = urlsplit(self._url)
        return self._components

    @property
    def transport(self) -> str:
        return self.components.scheme

    @property
    def username(self) -> typing.Optional[str]:
        return self.components.username

    @property
    def password(self) -> typing.Optional[str]:
        return self.components.password

    @property
    def hostname(self) -> typing.Optional[str]:
        return self.components.hostname

    @property
    def port(self) -> typing.Optional[int]:
        return self.components.port

    @property
    def netloc(self) -> typing.Optional[str]:
        return self.components.netloc

    @property
    def path(self) -> typing.Optional[str]:
        return self.components.path

    @property
    def options(self) -> dict:
        if not hasattr(self, "_options"):
            options = dict(parse_qsl(self.components.query))
            self._options = options
        return self._options

    def replace(self, **kwargs: typing.Any) -> "EmailURL":
        if (
                "username" in kwargs
                or "password" in kwargs
                or "hostname" in kwargs
                or "port" in kwargs
        ):
            hostname = kwargs.pop("hostname", self.hostname)
            port = kwargs.pop("port", self.port)
            username = kwargs.pop("username", self.username)
            password = kwargs.pop("password", self.password)

            netloc = hostname
            if port is not None:
                netloc += f":{port}"
            if username is not None:
                userpass = username
                if password is not None:
                    userpass += f":{password}"
                netloc = f"{userpass}@{netloc}"

            kwargs["netloc"] = netloc

        if "transport" in kwargs:
            transport = kwargs.pop("transport", self.transport)
            kwargs["scheme"] = f"{transport}"

        components = self.components._replace(**kwargs)
        return self.__class__(components.geturl())

    def __str__(self) -> str:
        return self._url

    def __repr__(self) -> str:
        url = str(self)
        if self.password:
            url = str(self.replace(password="********"))
        return f"{self.__class__.__name__}({repr(url)})"

    def __eq__(self, other: typing.Any) -> bool:
        return str(self) == str(other)
