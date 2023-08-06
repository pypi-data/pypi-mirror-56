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

"""Flask Native URL Normalizing Middleware."""


class URLNormalizingMiddleware(object):
    """Middleware filter to handle URL normalization."""

    # NOTE(morgan): This must be a middleware as changing 'PATH_INFO' after
    # the request hits the flask app will not impact routing.

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        """Normalize URLs."""
        # TODO(morgan): evaluate collapsing multiple slashes in this middleware
        # e.g. '/v3//auth/tokens -> /v3/auth/tokens

        # Removes a trailing slashes from the given path, if any.
        if len(environ['PATH_INFO']) > 1 and environ['PATH_INFO'][-1] == '/':
            environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')

        # Rewrites path to root if no path is given
        if not environ['PATH_INFO']:
            environ['PATH_INFO'] = '/'

        return self.app(environ, start_response)
