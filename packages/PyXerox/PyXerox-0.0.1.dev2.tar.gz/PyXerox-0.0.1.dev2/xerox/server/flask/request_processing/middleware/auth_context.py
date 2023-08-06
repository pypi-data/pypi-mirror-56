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

from keystonemiddleware import auth_token
from oslo_log import log

from xerox.common import authorization
from xerox.common import context
from xerox.common import provider_api
import xerox.conf

CONF = xerox.conf.CONF
LOG = log.getLogger(__name__)
PROVIDERS = provider_api.ProviderAPIs

# Environment variable used to pass the request context
CONTEXT_ENV = 'openstack.context'

__all__ = ('AuthContextMiddleware',)


class AuthContextMiddleware(provider_api.ProviderAPIMixin,
                            auth_token.BaseAuthProtocol):
    """Build the authentication context from the request auth token."""

    def __init__(self, app):
        super(AuthContextMiddleware, self).__init__(app, log=LOG,
                                                    service_type='xerox')
        self.token = None

    def process_request(self, request):
        # The request context stores itself in thread-local memory for logging.
        if authorization.AUTH_CONTEXT_ENV in request.environ:
            msg = ('Auth context already exists in the request '
                   'environment; it will be used for authorization '
                   'instead of creating a new one.')
            LOG.warning(msg)
            return

        kwargs = {
            'authenticated': True,
            'overwrite': True}
        request_context = context.RequestContext.from_environ(
            request.environ, **kwargs)
        request.environ[context.REQUEST_CONTEXT_ENV] = request_context

        # Create auth context for policy enforcer
        auth_context = request_context.to_policy_values()
        LOG.debug('RBAC: auth_context: %s', auth_context)

        request.environ[authorization.AUTH_CONTEXT_ENV] = auth_context

    @classmethod
    def factory(cls, global_config, **local_config):
        """Used for loading in middleware (holdover from paste.deploy)."""
        def _factory(app):
            conf = global_config.copy()
            conf.update(local_config)
            return cls(app, **local_config)
        return _factory
