# The MIT License
#
# Copyright (c) 2019 imuxin https://github.com/imuxin.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from oslo_log import log
from oslo_utils import encodeutils
import six
from six.moves import http_client

import xerox.conf
from xerox.i18n import _


CONF = xerox.conf.CONF
LOG = log.getLogger(__name__)

XEROX_API_EXCEPTIONS = set([])

# Tests use this to make exception message format errors fatal
_FATAL_EXCEPTION_FORMAT_ERRORS = False


def _format_with_unicode_kwargs(msg_format, kwargs):
    try:
        return msg_format % kwargs
    except UnicodeDecodeError:
        try:
            kwargs = {k: encodeutils.safe_decode(v)
                      for k, v in kwargs.items()}
        except UnicodeDecodeError:
            # NOTE(jamielennox): This is the complete failure case
            # at least by showing the template we have some idea
            # of where the error is coming from
            return msg_format

        return msg_format % kwargs


class _XeroxExceptionMeta(type):
    """Automatically Register the Exceptions in 'XEROX_API_EXCEPTIONS' list.

    The `XEROX_API_EXCEPTIONS` list is utilized by flask to register a
    handler to emit sane details when the exception occurs.
    """

    def __new__(mcs, name, bases, class_dict):
        """Create a new instance and register with XEROX_API_EXCEPTIONS."""
        cls = type.__new__(mcs, name, bases, class_dict)
        XEROX_API_EXCEPTIONS.add(cls)
        return cls


@six.add_metaclass(_XeroxExceptionMeta)
class Error(Exception):
    """Base error class.

    Child classes should define an HTTP status code, title, and a
    message_format.

    """

    code = None
    title = None
    message_format = None

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            # if you see this warning in your logs, please raise a bug report
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                LOG.warning('missing exception kwargs (programmer error)')
                message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Build and returns an exception message.

        :raises KeyError: given insufficient kwargs

        """
        if message:
            return message
        return _format_with_unicode_kwargs(self.message_format, kwargs)


class ValidationError(Error):
    message_format = _("Expecting to find %(attribute)s in %(target)s."
                       " The server could not comply with the request"
                       " since it is either malformed or otherwise"
                       " incorrect. The client is assumed to be in error.")
    code = int(http_client.BAD_REQUEST)
    title = http_client.responses[http_client.BAD_REQUEST]


class SchemaValidationError(ValidationError):
    # NOTE(lbragstad): For whole OpenStack message consistency, this error
    # message has been written in a format consistent with WSME.
    message_format = _("%(detail)s")


class ValidationTimeStampError(Error):
    message_format = _("Timestamp not in expected format."
                       " The server could not comply with the request"
                       " since it is either malformed or otherwise"
                       " incorrect. The client is assumed to be in error.")
    code = int(http_client.BAD_REQUEST)
    title = http_client.responses[http_client.BAD_REQUEST]


class ValidationExpirationError(Error):
    message_format = _("The 'expires_at' must not be before now."
                       " The server could not comply with the request"
                       " since it is either malformed or otherwise"
                       " incorrect. The client is assumed to be in error.")
    code = int(http_client.BAD_REQUEST)
    title = http_client.responses[http_client.BAD_REQUEST]


class StringLengthExceeded(ValidationError):
    message_format = _("String length exceeded. The length of"
                       " string '%(string)s' exceeds the limit"
                       " of column %(type)s(CHAR(%(length)d)).")


class SecurityError(Error):
    """Security error exception.

    Avoids exposing details of security errors, unless in insecure_debug mode.

    """

    amendment = _('(Disable insecure_debug mode to suppress these details.)')

    def __deepcopy__(self):
        """Override the default deepcopy.

        Xerox :class:`xerox.exception.Error` accepts an optional message
        that will be used when rendering the exception object as a string. If
        not provided the object's message_format attribute is used instead.
        :class:`xerox.exception.SecurityError` is a little different in
        that it only uses the message provided to the initializer when
        xerox is in `insecure_debug` mode. Instead it will use its
        `message_format`. This is to ensure that sensitive details are not
        leaked back to the caller in a production deployment.

        This dual mode for string rendering causes some odd behaviour when
        combined with oslo_i18n translation. Any object used as a value for
        formatting a translated string is deep copied.

        The copy causes an issue. The deep copy process actually creates a new
        exception instance with the rendered string. Then when that new
        instance is rendered as a string to use for substitution a warning is
        logged. This is because the code tries to use the `message_format` in
        secure mode, but the required kwargs are not in the deep copy.

        The end result is not an error because when the KeyError is caught the
        instance's ``message`` is used instead and this has the properly
        translated message. The only indication that something is wonky is a
        message in the warning log.
        """
        return self

    def _build_message(self, message, **kwargs):
        """Only returns detailed messages in insecure_debug mode."""
        if message and CONF.insecure_debug:
            if isinstance(message, six.string_types):
                # Only do replacement if message is string. The message is
                # sometimes a different exception or bytes, which would raise
                # TypeError.
                message = _format_with_unicode_kwargs(message, kwargs)
            return _('%(message)s %(amendment)s') % {
                'message': message,
                'amendment': self.amendment}

        return _format_with_unicode_kwargs(self.message_format, kwargs)


class Unauthorized(SecurityError):
    message_format = _("The request you have made requires authentication.")
    code = int(http_client.UNAUTHORIZED)
    title = http_client.responses[http_client.UNAUTHORIZED]


class AccountLocked(Unauthorized):
    message_format = _("The account is locked for user: %(user_id)s.")


class Forbidden(SecurityError):
    message_format = _("You are not authorized to perform the"
                       " requested action.")
    code = int(http_client.FORBIDDEN)
    title = http_client.responses[http_client.FORBIDDEN]


class ForbiddenAction(Forbidden):
    message_format = _("You are not authorized to perform the"
                       " requested action: %(action)s.")


class NotFound(Error):
    message_format = _("Could not find: %(target)s.")
    code = int(http_client.NOT_FOUND)
    title = http_client.responses[http_client.NOT_FOUND]


class LanguageNotFound(NotFound):
    message_format = _("Could not find language: %(language_id)s.")


class Conflict(Error):
    message_format = _("Conflict occurred attempting to store %(type)s -"
                       " %(details)s.")
    code = int(http_client.CONFLICT)
    title = http_client.responses[http_client.CONFLICT]


class UnexpectedError(SecurityError):
    """Avoids exposing details of failures, unless in insecure_debug mode."""

    message_format = _("An unexpected error prevented the server "
                       "from fulfilling your request.")

    debug_message_format = _("An unexpected error prevented the server "
                             "from fulfilling your request: %(exception)s.")

    def _build_message(self, message, **kwargs):

        # Ensure that exception has a value to be extra defensive for
        # substitutions and make sure the exception doesn't raise an
        # exception.
        kwargs.setdefault('exception', '')

        return super(UnexpectedError, self)._build_message(
            message or self.debug_message_format, **kwargs)

    code = int(http_client.INTERNAL_SERVER_ERROR)
    title = http_client.responses[http_client.INTERNAL_SERVER_ERROR]


class NotImplemented(Error):
    message_format = _("The action you have requested has not"
                       " been implemented.")
    code = int(http_client.NOT_IMPLEMENTED)
    title = http_client.responses[http_client.NOT_IMPLEMENTED]
