class MailablesError(Exception):
    pass


class SMTPError(MailablesError):
    pass


class DependencyNotFound(MailablesError):
    pass


class ImportFromStringError(MailablesError):
    pass


class UnsupportedTransportError(MailablesError):
    pass


class BadHeaderError(MailablesError):
    pass
