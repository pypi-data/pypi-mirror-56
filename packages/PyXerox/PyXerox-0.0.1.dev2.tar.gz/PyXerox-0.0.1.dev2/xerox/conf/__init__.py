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

import logging

from oslo_cache import core as cache
from oslo_config import cfg
from oslo_log import log
from oslo_log import versionutils
import oslo_messaging
from oslo_middleware import cors
from osprofiler import opts as profiler

from xerox.conf import default
from xerox.conf import program
from xerox.conf import wsgi

CONF = cfg.CONF


conf_modules = [
    default,
    program,
    wsgi
]


oslo_messaging.set_transport_defaults(control_exchange='xerox')
_DEPRECATED_REASON = ('This option is only used by eventlet mode which has '
                      'been removed from xerox in Newton release.')


def set_default_for_default_log_levels():
    """Set the default for the default_log_levels option for xerox.

    xerox uses some packages that other OpenStack services don't use that do
    logging. This will set the default_log_levels default level for those
    packages.

    This function needs to be called before CONF().

    """
    extra_log_level_defaults = [
        'dogpile=INFO',
        'routes=INFO',
    ]

    log.register_options(CONF)
    log.set_defaults(default_log_levels=log.get_default_log_levels() +
                     extra_log_level_defaults)


def setup_logging():
    """Set up logging for the xerox package."""
    log.setup(CONF, 'xerox')
    logging.captureWarnings(True)


def configure(conf=None):
    if conf is None:
        conf = CONF

    conf.register_cli_opt(
        cfg.BoolOpt('standard-threads', default=False,
                    help='Do not monkey-patch threading system modules.',
                    deprecated_for_removal=True,
                    deprecated_reason=_DEPRECATED_REASON,
                    deprecated_since=versionutils.deprecated.STEIN))
    conf.register_cli_opt(
        cfg.StrOpt('pydev-debug-host',
                   help='Host to connect to for remote debugger.',
                   deprecated_for_removal=True,
                   deprecated_reason=_DEPRECATED_REASON,
                   deprecated_since=versionutils.deprecated.STEIN))
    conf.register_cli_opt(
        cfg.PortOpt('pydev-debug-port',
                    help='Port to connect to for remote debugger.',
                    deprecated_for_removal=True,
                    deprecated_reason=_DEPRECATED_REASON,
                    deprecated_since=versionutils.deprecated.STEIN))

    for module in conf_modules:
        module.register_opts(conf)

    # add oslo.cache related config options
    cache.configure(conf)


def set_external_opts_defaults():
    """Update default configuration options for oslo.middleware."""
    cors.set_defaults(
        allow_headers=['X-Auth-Token',
                       'X-Openstack-Request-Id',
                       'X-Subject-Token',
                       'X-Project-Id',
                       'X-Project-Name',
                       'X-Project-Domain-Id',
                       'X-Project-Domain-Name',
                       'X-Domain-Id',
                       'X-Domain-Name',
                       'Openstack-Auth-Receipt'],
        expose_headers=['X-Auth-Token',
                        'X-Openstack-Request-Id',
                        'X-Subject-Token',
                        'Openstack-Auth-Receipt'],
        allow_methods=['GET',
                       'PUT',
                       'POST',
                       'DELETE',
                       'PATCH']
    )

    # configure OSprofiler options
    profiler.set_defaults(CONF, enabled=False, trace_sqlalchemy=False)

    # Oslo.cache is always enabled by default for request-local caching
    # TODO(morganfainberg): Fix this to not use internal interface when
    # oslo.cache has proper interface to set defaults added. This is
    # just a bad way to do this.
    opts = cache._opts.list_opts()
    for opt_list in opts:
        if opt_list[0] == 'cache':
            for o in opt_list[1]:
                if o.name == 'enabled':
                    o.default = True


def set_config_defaults():
    """Override all configuration default values for xerox."""
    set_default_for_default_log_levels()
    set_external_opts_defaults()
