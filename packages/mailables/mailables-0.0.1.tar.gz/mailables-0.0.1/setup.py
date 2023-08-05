# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mailables']

package_data = \
{'': ['*']}

extras_require = \
{'aiofiles': ['aiofiles>=0.4.0,<0.5.0'],
 'aiosmtplib': ['aiosmtplib>=1.1,<2.0'],
 'full': ['aiofiles>=0.4.0,<0.5.0', 'aiosmtplib>=1.1,<2.0']}

setup_kwargs = {
    'name': 'mailables',
    'version': '0.0.1',
    'description': 'Python emails for asynchronous world.',
    'long_description': '<p align="center">\n<a href="https://travis-ci.org/alex-oleshkevich/mailables">\n    <img src="https://api.travis-ci.com/alex-oleshkevich/mailables.svg?branch=master" alt="Build Status">\n</a>\n<a href="https://codecov.io/gh/alex-oleshkevich/mailables">\n    <img src="https://codecov.io/gh/alex-oleshkevich/mailables/branch/master/graph/badge.svg" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/mailables/">\n    <img src="https://badge.fury.io/py/starlette.svg" alt="Package version">\n</a>\n</p>\n\n---\n\n\n# Introduction\n\n`mailables` is a developer-centric package for sending asynchronous mails.\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n```shell\n$ pip install mailables\n```\n\n## Usage\n\n```python\nfrom mailables import Mailer, EmailMessage\n\nmessage = EmailMessage(\n    to=\'User Name <user@example.com>\',\n    from_address=\'sender@example.com\',\n    subject=\'Hey\',\n    text_body=\'This is sent using mailables!\',\n    html_body=\'<b>This is sent using mailables!</b>\'\n)\n\nmailer = Mailer(\'smtp://localhost:25\')\nawait mailer.send(message)\n```\n\n## Dependencies\n\nMailables does not have any hard dependencies, but the following are optional:\n\n* [`aiofiles`](https://github.com/Tinche/aiofiles) - required by `FileTransport`.\n* [`aiosmtpdlib`](https://github.com/cole/aiosmtplib) - required by `SMTPTransport`.\n\nYou can install all of these with `pip install mailables[full]`.\n\n\n## Configuration\n\nIn order to send email you need to configure transport and mailer.\nMailer is a class with which you would work all time. Think it is a public interface to `mailables`.\nAnd transport is a concrete adapter which does actual sending. \n\n```python\nfrom mailables import Mailer\n\nmailer = Mailer(\'smtp://localhost:25\')\n```\n\nWhen you need to fine-grained control on the transport configuration \nyou may pass the transport instance instead of URL string:\n\n```python\nfrom mailables import Mailer, SMTPTransport\nmailer = Mailer(SMTPTransport(host=\'localhost\', port=25))\n``` \n\nThis approach gives you full control on transport construction.\n\nNote, that you are not limited to one mailer only, \nyour application may have multiple mailers with different transports/settings. \n\n\n## Mail message\n\nThe mail message is represented by `EmailMessage` class.\n\n```python\nfrom mailables import EmailMessage\n\nmessage = EmailMessage(\n    to=[\'root@localhost\', \'admin@localhost\'],\n    from_address=\'user@localhost\',\n    subject=\'This is a test email\',\n    text_body=\'And this is a body\',\n    html_body=\'And HTML body <b>supported</b> as well\',\n)\n```  \n\n### Attaching files\n\n\n```python\nfrom mailables import EmailMessage, Attachment\n\nmessage = EmailMessage(\n    attachments=[\n        Attachment(contents=\'CONTENTS\', file_name=\'file.txt\')        \n    ]\n)\n\n# or alternatively using `attach` method:\nmessage.attach(contents=\'CONTENTS\', file_name=\'file.txt\')\n\n# or you can add attachment instance using `add_attachment` method:\nmessage.add_attachment(Attachment(\'contents\'))\n```\n \n### Attaching files\n\nNote, that reading files is blocking process and is harmful in asynchronous \nenvironment. You may want to use libraries like [`aiofiles`](https://github.com/Tinche/aiofiles)\nto read files without blocking the thread.\n\n```python\nfrom mailables import EmailMessage\n\nwith open(\'/path/to/file.txt\') as f:\n    message = EmailMessage()\n    message.attach(f.read())\n```\n \n\n## Transports\n\nHere is the list of included transports\n\n### SMTPTransport\n\nSends messages using SMTP protocol.\n\n```python\nfrom mailables import SMTPTransport\n\ntransport = SMTPTransport(host=\'localhost\', port=25, use_ssl=True)\n```\n\n### FileTransport\n\nFile transport does not send email to anywhere. It dumps messages into mailbox directory in `*.eml` format.\n\n```python\nfrom mailables import FileTransport\n\ntransport = FileTransport(directory=\'/tmp/mailbox\')\n```\n\n### InMemoryTransport\n\nStores sent emails in a local variable.\n\n```python\nfrom mailables import InMemoryTransport, EmailMessage\n\nstorage = []\ntransport = InMemoryTransport(storage=storage)\n\n# example:\ntransport.send(EmailMessage(subject=\'Hey\', to=\'root@localhost\'))\nassert len(storage) == 1\n```\n\n### NullTransport\n\nThis transport does not send anything at all. Use it when you want to completely silence the mailer.\n\n```python\nfrom mailables import NullTransport\n\ntransport = NullTransport()\n```\n\n\n## Building custom transports\n\nExtend `mailables.transport.BaseTransport` class and \nimplement `async def send(self, message: EmailMessage)` method:\n\nFor example, we will create a simple transport class for writing mails to a stdout:\n\n```python\nfrom mailables import BaseTransport, EmailMessage, Mailer\n\nclass ConsoleTransport(BaseTransport):\n    async def send(self, message: EmailMessage):\n        print(str(message))\n\n\nmailer = Mailer(ConsoleTransport())\n```\n',
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@muehlemann-popp.ch',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
