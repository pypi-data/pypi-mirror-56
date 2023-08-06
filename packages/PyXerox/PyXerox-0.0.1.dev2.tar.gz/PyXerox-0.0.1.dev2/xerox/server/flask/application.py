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

from __future__ import absolute_import

import functools
import sys

import flask
import oslo_i18n
from oslo_log import log
from oslo_middleware import healthcheck
import six

try:
    # werkzeug 0.15.x
    from werkzeug.middleware import dispatcher as wsgi_dispatcher
except ImportError:
    # werkzeug 0.14.x
    import werkzeug.wsgi as wsgi_dispatcher

import xerox.api
from xerox import exception
from xerox.server.flask import common as ks_flask
from xerox.server.flask.request_processing import json_body
from xerox.server.flask.request_processing import req_logging

# from xerox.receipt import handlers as receipt_handlers

LOG = log.getLogger(__name__)


def fail_gracefully(f):
    """Log exceptions and aborts."""
    @functools.wraps(f)
    def wrapper(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            LOG.debug(e, exc_info=True)

            # exception message is printed to all logs
            LOG.critical(e)
            sys.exit(1)

    return wrapper


def _add_vary_x_auth_token_header(response):
    # Add the expected Vary Header, this is run after every request in the
    # response-phase
    response.headers['Vary'] = 'X-Auth-Token'
    return response


def _best_match_language():
    """Determine the best available locale.

    This returns best available locale based on the Accept-Language HTTP
    header passed in the request.
    """
    if not flask.request.accept_languages:
        return None
    return flask.request.accept_languages.best_match(
        oslo_i18n.get_available_languages('xerox'))


def _handle_xerox_exception(error):
    # TODO(adriant): register this with its own specific handler:
    # if isinstance(error, exception.InsufficientAuthMethods):
    #     return receipt_handlers.build_receipt(error)

    # Handle logging
    if isinstance(error, exception.Unauthorized):
        LOG.warning(
            "Authorization failed. %(exception)s from %(remote_addr)s",
            {'exception': error, 'remote_addr': flask.request.remote_addr})
    elif isinstance(error, exception.UnexpectedError):
        LOG.exception(six.text_type(error))
    else:
        LOG.warning(six.text_type(error))

    # Render the exception to something user "friendly"
    error_message = error.args[0]
    message = oslo_i18n.translate(error_message, _best_match_language())
    if message is error_message:
        # translate() didn't do anything because it wasn't a Message,
        # convert to a string.
        message = six.text_type(message)

    body = dict(
        error={
            'code': error.code,
            'title': error.title,
            'message': message}
    )

    if isinstance(error, exception.AuthPluginException):
        body['error']['identity'] = error.authentication

    # Create the response and set status code.
    response = flask.jsonify(body)
    response.status_code = error.code

    # Add the appropriate WWW-Authenticate header for Unauthorized
    if isinstance(error, exception.Unauthorized):
        url = ks_flask.base_url()
        response.headers['WWW-Authenticate'] = 'Xerox uri="%s"' % url
    return response


def _handle_unknown_xerox_exception(error):
    # translate a python exception to something we can properly render as
    # an API error.
    if isinstance(error, TypeError):
        new_exc = exception.ValidationError(error)
    else:
        new_exc = exception.UnexpectedError(error)
    return _handle_xerox_exception(new_exc)


@fail_gracefully
def application_factory(name='public'):
    if name not in ('admin', 'public'):
        raise RuntimeError('Application name (for base_url lookup) must be '
                           'either `admin` or `public`.')

    app = flask.Flask(name)

    # Register Error Handler Function for Xerox Errors.
    # NOTE(morgan): Flask passes errors to an error handling function. All of
    # xerox's api errors are explicitly registered in
    # xerox.exception.XEROX_API_EXCEPTIONS and those are in turn
    # registered here to ensure a proper error is bubbled up to the end user
    # instead of a 500 error.
    for exc in exception.XEROX_API_EXCEPTIONS:
        app.register_error_handler(exc, _handle_xerox_exception)

    # Register extra (python) exceptions with the proper exception handler,
    # specifically TypeError. It will render as a 400 error, but presented in
    # a "web-ified" manner
    app.register_error_handler(TypeError, _handle_unknown_xerox_exception)

    # Add core before request functions
    app.before_request(req_logging.log_request_info)
    app.before_request(json_body.json_body_before_request)

    # Add core after request functions
    app.after_request(_add_vary_x_auth_token_header)

    # NOTE(morgan): Configure the Flask Environment for our needs.
    app.config.update(
        # We want to bubble up Flask Exceptions (for now)
        PROPAGATE_EXCEPTIONS=True)

    for api in xerox.api.__apis__:
        for api_bp in api.APIs:
            api_bp.instantiate_and_register_to_app(app)

    # Load in Healthcheck and map it to /healthcheck
    hc_app = healthcheck.Healthcheck.app_factory(
        {}, oslo_config_project='xerox')

    # Use the simple form of the dispatch middleware, no extra logic needed
    # for legacy dispatching. This is to mount /healthcheck at a consistent
    # place
    app.wsgi_app = wsgi_dispatcher.DispatcherMiddleware(
        app.wsgi_app,
        {'/healthcheck': hc_app})
    return app
