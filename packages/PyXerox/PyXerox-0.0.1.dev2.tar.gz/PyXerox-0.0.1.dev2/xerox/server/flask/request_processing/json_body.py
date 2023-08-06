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

"""Before request processing for JSON Body enforcement."""

import flask
from werkzeug import exceptions as werkzeug_exceptions

from xerox import exception
from xerox.i18n import _
from xerox.server.flask import common as ks_flask_common


def json_body_before_request():
    """Enforce JSON Request Body."""
    # TODO(morgan): Allow other content-types when OpenAPI Doc or improved
    # federation is implemented for known/valid paths. This function should
    # be removed long term.

    # exit if there is nothing to be done, (no body)
    if not flask.request.get_data():
        return None

    try:
        # flask does loading for us for json, use the flask default loader
        # in the case that the data is *not* json or a dict, we should see a
        # raise of werkzeug.exceptions.BadRequest, re-spin this to the xerox
        # ValidationError message (as expected by our contract)

        # Explicitly check if the content is supposed to be json.
        if (flask.request.is_json
                or flask.request.headers.get('Content-Type', '') == ''):
            json_decoded = flask.request.get_json(force=True)
            if not isinstance(json_decoded, dict):
                # In the case that the returned value was not a dict, force
                # a raise that will be caught the same way that a Decode error
                # would be handled.
                raise werkzeug_exceptions.BadRequest(
                    _('resulting JSON load was not a dict'))
        else:
            # We no longer need enforcement on this API, set unenforced_ok
            # we already hit a validation error. This is required as the
            # request is never hitting the resource methods, meaning
            # @unenforced_api is not called. Without marking the request
            # as "unenforced_ok" the assertion check to ensure enforcement
            # was called would raise up causing a 500 error.
            ks_flask_common.set_unenforced_ok()
            raise exception.ValidationError(attribute='application/json',
                                            target='Content-Type header')

    except werkzeug_exceptions.BadRequest:
        # We no longer need enforcement on this API, set unenforced_ok
        # we already hit a validation error. This is required as the
        # request is never hitting the resource methods, meaning
        # @unenforced_api is not called. Without marking the request
        # as "unenforced_ok" the assertion check to ensure enforcement
        # was called would raise up causing a 500 error.
        ks_flask_common.set_unenforced_ok()
        raise exception.ValidationError(attribute='valid JSON',
                                        target='request body')
