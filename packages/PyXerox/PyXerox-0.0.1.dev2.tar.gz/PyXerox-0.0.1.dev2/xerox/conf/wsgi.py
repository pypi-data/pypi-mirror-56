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

from oslo_config import cfg

from xerox.conf import utils


debug_middlware = cfg.BoolOpt(
    'debug_middleware',
    default=False,
    help=utils.fmt("""
If set to true, this enables the oslo debug middleware in Xerox. This
Middleware prints a lot of information about the request and the response. It
is useful for getting information about the data on the wire (decoded) and
passed to the WSGI application pipeline. This middleware has no effect on
the "debug" setting in the [DEFAULT] section of the config file or setting
Xerox's log-level to "DEBUG"; it is specific to debugging the WSGI data
as it enters and leaves Xerox (specific request-related data). This option
is used for introspection on the request and response data between the web
server (apache, nginx, etc) and Xerox.

This middleware is inserted as the first element in the middleware chain
and will show the data closest to the wire.

WARNING: NOT INTENDED FOR USE IN PRODUCTION. THIS MIDDLEWARE CAN AND WILL EMIT
SENSITIVE/PRIVILEGED DATA.
"""))

GROUP_NAME = __name__.split('.')[-1]
ALL_OPTS = [
    debug_middlware,
]


def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)


def list_opts():
    return {GROUP_NAME: ALL_OPTS}
