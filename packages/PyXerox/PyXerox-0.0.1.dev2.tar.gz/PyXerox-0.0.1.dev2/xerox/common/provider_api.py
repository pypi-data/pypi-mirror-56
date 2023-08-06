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


class ProviderAPIRegistry(object):
    __shared_object_state = {}
    __registry = {}
    __iter__ = __registry.__iter__
    __getitem__ = __registry.__getitem__
    locked = False

    def __init__(self):
        # NOTE(morgan): This rebinds __dict__ and allows all instances of
        # the provider API to share a common state. Any changes except
        # rebinding __dict__ will maintain the same state stored on the class
        # not the instance. This design pattern is preferable to
        # full singletons where state sharing is the important "feature"
        # derived from the "singleton"
        #
        # Use "super" to bypass the __setattr__ preventing changes to the
        # object itself.
        super(ProviderAPIRegistry, self).__setattr__(
            '__dict__', self.__shared_object_state)

    def __getattr__(self, item):
        """Do attr lookup."""
        try:
            return self.__registry[item]
        except KeyError:
            raise AttributeError(
                "'ProviderAPIs' has no attribute %s" % item)

    def __setattr__(self, key, value):
        """Do not allow setting values on the registry object."""
        raise RuntimeError('Programming Error: You may not set values on the '
                           'ProviderAPIRegistry objects.')

    def _register_provider_api(self, name, obj):
        """Register an instance of a class as a provider api."""
        if name == 'driver':
            raise ValueError('A provider may not be named "driver".')

        if self.locked:
            raise RuntimeError(
                'Programming Error: The provider api registry has been '
                'locked (post configuration). Ensure all provider api '
                'managers are instantiated before locking.')

        if name in self.__registry:
            raise DuplicateProviderError(
                '`%(name)s` has already been registered as an api '
                'provider by `%(prov)r`' % {'name': name,
                                            'prov': self.__registry[name]})
        self.__registry[name] = obj

    def _clear_registry_instances(self):
        """ONLY USED FOR TESTING."""
        self.__registry.clear()
        # Use super to allow setting around class implementation of __setattr__
        super(ProviderAPIRegistry, self).__setattr__('locked', False)

    def lock_provider_registry(self):
        # Use super to allow setting around class implementation of __setattr__
        super(ProviderAPIRegistry, self).__setattr__('locked', True)

    def deferred_provider_lookup(self, api, method):
        """Create descriptor that performs lookup of api and method on demand.

        For specialized cases, such as the enforcer "get_member_from_driver"
        which needs to be effectively a "classmethod", this method returns
        a smart descriptor object that does the lookup at runtime instead of
        at import time.

        :param api: The api to use, e.g. "identity_api"
        :type api: str
        :param method: the method on the api to return
        :type method: str
        """
        class DeferredProviderLookup(object):
            def __init__(self, api, method):
                self.__api = api
                self.__method = method

            def __get__(self, instance, owner):
                api = getattr(ProviderAPIs, self.__api)
                return getattr(api, self.__method)

        return DeferredProviderLookup(api, method)


class DuplicateProviderError(Exception):
    """Attempting to register a duplicate API provider."""


class ProviderAPIMixin(object):
    """Allow referencing provider apis on self via __getattr__.

    Be sure this class is first in the class definition for inheritance.
    """

    def __getattr__(self, item):
        """Magic getattr method."""
        try:
            return getattr(ProviderAPIs, item)
        except AttributeError:
            return self.__getattribute__(item)


ProviderAPIs = ProviderAPIRegistry()
