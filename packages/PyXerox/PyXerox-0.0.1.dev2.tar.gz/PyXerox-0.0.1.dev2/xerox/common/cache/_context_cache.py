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

"""A dogpile.cache proxy that caches objects in the request local cache."""
from dogpile.cache import api
from dogpile.cache import proxy
from oslo_context import context as oslo_context
from oslo_serialization import msgpackutils


# Register our new handler.
_registry = msgpackutils.default_registry


def _register_model_handler(handler_class):
    """Register a new model handler."""
    _registry.frozen = False
    _registry.register(handler_class(registry=_registry))
    _registry.frozen = True


class _ResponseCacheProxy(proxy.ProxyBackend):

    __key_pfx = '_request_cache_%s'

    def _get_request_context(self):
        # Return the current context or a new/empty context.
        return oslo_context.get_current() or oslo_context.RequestContext()

    def _get_request_key(self, key):
        return self.__key_pfx % key

    def _set_local_cache(self, key, value):
        # Set a serialized version of the returned value in local cache for
        # subsequent calls to the memoized method.
        ctx = self._get_request_context()
        serialize = {'payload': value.payload, 'metadata': value.metadata}
        setattr(ctx, self._get_request_key(key), msgpackutils.dumps(serialize))

    def _get_local_cache(self, key):
        # Return the version from our local request cache if it exists.
        ctx = self._get_request_context()
        try:
            value = getattr(ctx, self._get_request_key(key))
        except AttributeError:
            return api.NO_VALUE

        value = msgpackutils.loads(value)
        return api.CachedValue(payload=value['payload'],
                               metadata=value['metadata'])

    def _delete_local_cache(self, key):
        # On invalidate/delete remove the value from the local request cache
        ctx = self._get_request_context()
        try:
            delattr(ctx, self._get_request_key(key))
        except AttributeError:  # nosec
            # NOTE(morganfainberg): We will simply pass here, this value has
            # not been cached locally in the request.
            pass

    def get(self, key):
        value = self._get_local_cache(key)
        if value is api.NO_VALUE:
            value = self.proxied.get(key)
            if value is not api.NO_VALUE:
                self._set_local_cache(key, value)
        return value

    def set(self, key, value):
        self._set_local_cache(key, value)
        self.proxied.set(key, value)

    def delete(self, key):
        self._delete_local_cache(key)
        self.proxied.delete(key)

    def get_multi(self, keys):
        values = {}
        for key in keys:
            v = self._get_local_cache(key)
            if v is not api.NO_VALUE:
                values[key] = v
        query_keys = set(keys).difference(set(values.keys()))
        values.update(dict(
            zip(query_keys, self.proxied.get_multi(query_keys))))
        return [values[k] for k in keys]

    def set_multi(self, mapping):
        for k, v in mapping.items():
            self._set_local_cache(k, v)
        self.proxied.set_multi(mapping)

    def delete_multi(self, keys):
        for k in keys:
            self._delete_local_cache(k)
        self.proxied.delete_multi(keys)
