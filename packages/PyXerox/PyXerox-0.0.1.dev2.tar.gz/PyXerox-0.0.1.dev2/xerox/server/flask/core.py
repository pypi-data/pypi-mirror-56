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

import collections
import os

from oslo_log import log
import stevedore

try:
    # werkzeug 0.15.x
    from werkzeug.middleware import proxy_fix
except ImportError:
    # werkzeug 0.14.x
    from werkzeug.contrib import fixers as proxy_fix

from xerox.common import profiler
import xerox.conf
import xerox.server
from xerox.server.flask import application
from xerox.server.flask.request_processing.middleware import auth_context
from xerox.server.flask.request_processing.middleware import url_normalize

# NOTE(morgan): Middleware Named Tuple with the following values:
#   * "namespace": namespace for the entry_point
#   * "ep": the entry-point name
#   * "conf": extra config data for the entry_point (None or Dict)
_Middleware = collections.namedtuple('LoadableMiddleware',
                                     'namespace, ep, conf')


CONF = xerox.conf.CONF
# NOTE(morgan): ORDER HERE IS IMPORTANT! The middleware will process the
# request in this list's order.
_APP_MIDDLEWARE = (
    _Middleware(namespace='xerox.server_middleware',
                ep='cors',
                conf={'oslo_config_project': 'xerox'}),
    _Middleware(namespace='xerox.server_middleware',
                ep='sizelimit',
                conf={}),
    _Middleware(namespace='xerox.server_middleware',
                ep='http_proxy_to_wsgi',
                conf={}),
    _Middleware(namespace='xerox.server_middleware',
                ep='osprofiler',
                conf={}),
    _Middleware(namespace='xerox.server_middleware',
                ep='request_id',
                conf={}),
    _Middleware(namespace='xerox.server_middleware',
                ep='authtoken',
                conf={}),
)

# NOTE(morgan): ORDER HERE IS IMPORTANT! Each of these middlewares are
# implemented/defined explicitly in Xerox Server. They do some level of
# lifting to ensure the request is properly handled. It is importat to note
# that these will be processed in the order of this list AND after all
# middleware defined in _APP_MIDDLEWARE. AuthContextMiddleware should always
# be the last element here as long as it is an actual Middleware.
_XEROX_MIDDLEWARE = (
    auth_context.AuthContextMiddleware,
    url_normalize.URLNormalizingMiddleware,
)


def _get_config_files(env=None):
    if env is None:
        env = os.environ

    dirname = env.get('OS_XEROX_CONFIG_DIR', '').strip()

    files = [s.strip() for s in
             env.get('OS_XEROX_CONFIG_FILES', '').split(';') if s.strip()]

    if dirname:
        if not files:
            files = ['xerox.conf']
        files = [os.path.join(dirname, fname) for fname in files]

    return files


def setup_app_middleware(app):
    # NOTE(morgan): Load the middleware, in reverse order, we wrap the app
    # explicitly; reverse order to ensure the first element in _APP_MIDDLEWARE
    # processes the request first.

    MW = _APP_MIDDLEWARE
    IMW = _XEROX_MIDDLEWARE

    # Add in optional (config-based) middleware
    # NOTE(morgan): Each of these may need to be in a specific location
    # within the pipeline therefore cannot be magically appended/prepended
    if CONF.wsgi.debug_middleware:
        # Add in the Debug Middleware
        MW += (_Middleware(namespace='xerox.server_middleware',
                           ep='debug',
                           conf={}),)

    # Apply internal-only Middleware (e.g. AuthContextMiddleware). These
    # are below all externally loaded middleware in request processing.
    for mw in reversed(IMW):
        app.wsgi_app = mw(app.wsgi_app)

    # Apply the middleware to the application.
    for mw in reversed(MW):
        # TODO(morgan): Explore moving this to ExtensionManager, but we
        # want to be super careful about what middleware we load and in
        # what order. DriverManager gives us that capability and only loads
        # the entry points we care about rather than all of them.

        # Load via Stevedore, initialize the class via the factory so we can
        # initialize the "loaded" entrypoint with the currently bound
        # object pointed at "application". We may need to eventually move away
        # from the "factory" mechanism.
        loaded = stevedore.DriverManager(
            mw.namespace, mw.ep, invoke_on_load=False)
        # NOTE(morgan): global_conf (args[0]) to the factory is always empty
        # and local_conf (args[1]) will be the mw.conf dict. This allows for
        # configuration to be passed for middleware such as oslo CORS which
        # expects oslo_config_project or "allowed_origin" to be in the
        # local_conf, this is all a hold-over from paste-ini and pending
        # reworking/removal(s)
        if hasattr(loaded.driver, 'factory'):
            factory_func = loaded.driver.factory({}, **mw.conf)
        else:
            # the provided filter is not standard mw in this definition.
            factory_func = loaded.driver({}, **mw.conf)
        app.wsgi_app = factory_func(app.wsgi_app)

    # Apply werkzeug specific middleware
    app.wsgi_app = proxy_fix.ProxyFix(app.wsgi_app)
    return app


def initialize_application(name, post_log_configured_function=lambda: None,
                           config_files=None):
    def _initialize_configuration(config_files=config_files):
        possible_topdir = os.path.normpath(os.path.join(
                                           os.path.abspath(__file__),
                                           os.pardir,
                                           os.pardir,
                                           os.pardir,
                                           os.pardir))

        dev_conf = os.path.join(possible_topdir,
                                'etc',
                                'xerox.conf')
        if not config_files:
            config_files = None
            if os.path.exists(dev_conf):
                config_files = [dev_conf]

        xerox.server.configure(config_files=config_files)

        # Log the options used when starting if we're in debug mode...
        if CONF.debug:
            CONF.log_opt_values(log.getLogger(CONF.prog), log.DEBUG)

    _initialize_configuration()
    post_log_configured_function()

    # TODO(morgan): Provide a better mechanism than "loadapp", this was for
    # paste-deploy specific mechanisms.
    def _loadapp():
        app = application.application_factory(name)
        return app

    _unused, app = xerox.server.setup_backends(
        startup_application_fn=_loadapp)

    # setup OSprofiler notifier and enable the profiling if that is configured
    # in Xerox configuration file.
    profiler.setup(name)

    return setup_app_middleware(app)
