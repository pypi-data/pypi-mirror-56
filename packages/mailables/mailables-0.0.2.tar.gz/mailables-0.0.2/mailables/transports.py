import abc
import datetime
import os
import ssl
from typing import List, Union

from mailables.config import EmailURL, SUPPORTED_BACKENDS
from mailables.exceptions import DependencyNotFound, UnsupportedTransportError
from mailables.importer import import_from_string
from mailables.message import EmailMessage

try:
    import aiofiles
except ImportError:  # pragma: nocover
    aiofiles = None

try:
    import aiosmtplib
except ImportError:  # pragma: nocover
    aiosmtplib = None


class BaseTransport(abc.ABC):
    @abc.abstractmethod
    async def send(self, message: EmailMessage):  # pragma: nocover
        raise NotImplementedError()


class FileTransport(BaseTransport):
    def __init__(self, directory: str):
        if aiofiles is None:
            raise DependencyNotFound('%s requires "aiofiles" library installed.' % self.__class__.__name__)
        self._directory = directory

    async def send(self, message: EmailMessage):
        import aiofiles
        file_name = 'message_%s.eml' % datetime.datetime.today().isoformat()
        output_file = os.path.join(self._directory, file_name)
        async with aiofiles.open(output_file, 'wb') as stream:
            await stream.write(message.as_string().encode('utf8'))


class NullTransport(BaseTransport):
    async def send(self, message: EmailMessage):
        pass


class InMemoryTransport(BaseTransport):
    @property
    def mailbox(self) -> List[EmailMessage]:
        return self._storage

    def __init__(self, storage: List[EmailMessage]):
        self._storage = storage

    async def send(self, message: EmailMessage):
        self._storage.append(message)


class SMTPTransport(BaseTransport):
    def __init__(
            self, host: str = 'localhost', port: int = 25, user: str = None, password: str = None,
            use_ssl: bool = None, timeout: int = 10, key_file: str = None, cert_file: str = None,
    ):
        if aiosmtplib is None:
            print(self.__class__.__name__)
            raise DependencyNotFound('%s requires "aiosmtplib" library installed.' % self.__class__.__name__)

        self._host = host
        self._user = user
        self._port = port
        self._password = password
        self._use_ssl = use_ssl
        self._timeout = timeout
        self._key_file = key_file
        self._cert_file = cert_file

    async def send(self, message: EmailMessage):
        context = ssl.create_default_context()
        client = aiosmtplib.SMTP(
            hostname=self._host,
            port=self._port,
            use_tls=self._use_ssl,
            username=self._user,
            password=self._password,
            timeout=self._timeout,
            tls_context=context,
            client_key=self._key_file,
            client_cert=self._cert_file,
        )
        async with client:
            await client.send_message(message.build_message())


def create_transport(url: Union[str, EmailURL]) -> BaseTransport:
    url = EmailURL(str(url))

    if url.transport not in SUPPORTED_BACKENDS:
        raise UnsupportedTransportError(
            f'No transport found with scheme "{url.transport}".'
        )
    factory = import_from_string(SUPPORTED_BACKENDS[url.transport])
    return factory(url)


def file_transport_factory(url: EmailURL) -> FileTransport:
    return FileTransport(url.path)


def null_transport_factory(*args) -> NullTransport:
    return NullTransport()


def memory_transport_factory(url: EmailURL) -> InMemoryTransport:
    return InMemoryTransport([])


def _cast_to_bool(value: str) -> bool:
    return value.lower() in ['yes', '1', 'on', 'true']


def smtp_transport_factory(url: EmailURL) -> SMTPTransport:
    timeout = url.options.get('timeout', None)
    if timeout:
        timeout = int(timeout)

    use_ssl = _cast_to_bool(url.options.get('use_ssl', ''))
    key_file = url.options.get('key_file', None)
    cert_file = url.options.get('cert_file', None)

    return SMTPTransport(
        url.hostname, url.port, url.username, url.password,
        use_ssl=use_ssl, timeout=timeout, key_file=key_file, cert_file=cert_file,
    )
