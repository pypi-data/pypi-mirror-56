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

from xerox.common import cache
from xerox.common import provider_api
from xerox import program

LOG = log.getLogger(__name__)


def load_backends():

    # Configure and build the cache
    cache.configure_cache()
    # cache.configure_cache(region=catalog.COMPUTED_CATALOG_REGION)
    # cache.configure_cache(region=assignment.COMPUTED_ASSIGNMENTS_REGION)
    # cache.configure_cache(region=revoke.REVOKE_REGION)
    # cache.configure_cache(region=token.provider.TOKENS_REGION)
    # cache.configure_cache(region=receipt.provider.RECEIPTS_REGION)
    # cache.configure_cache(region=identity.ID_MAPPING_REGION)
    cache.configure_invalidation_region()

    managers = [program.Manager]

    drivers = {d._provides_api: d() for d in managers}

    # NOTE(morgan): lock the APIs, these should only ever be instantiated
    # before running xerox.
    provider_api.ProviderAPIs.lock_provider_registry()

    return drivers
