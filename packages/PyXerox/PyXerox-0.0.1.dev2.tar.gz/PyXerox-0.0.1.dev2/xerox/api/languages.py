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

import flask
from six.moves import http_client

from xerox.common import provider_api
from xerox.common import rbac_enforcer
from xerox.common import validation
from xerox import exception as ks_exception
from xerox.program import schema
from xerox.server import flask as x_flask


ENFORCER = rbac_enforcer.RBACEnforcer
PROVIDERS = provider_api.ProviderAPIs


def _build_language_target_enforcement():
    target = {}
    try:
        target['language'] = PROVIDERS.program_api.get_language(
            flask.request.view_args.get('language_id')
        )
    except ks_exception.NotFound:  # nosec
        # Defer existence in the event the language doesn't exist, we'll
        # check this later anyway.
        pass

    return target


class LanguageResource(x_flask.ResourceBase):
    collection_key = 'languages'
    member_key = 'language'
    get_member_from_driver = PROVIDERS.deferred_provider_lookup(
        api='program_api', method='get_language')

    def get(self, language_id=None):
        """Get an language resource or list languages.

        GET/HEAD /1/languages
        GET/HEAD /v1/languages/{language_id}
        """
        if language_id is not None:
            return self._get_language(language_id)
        return self._list_languages()

    def _get_language(self, language_id):
        """Get an language resource.

        GET/HEAD /v1/languages/{language_id}
        """
        ENFORCER.enforce_call(
            action='xerox:get_language',
            build_target=_build_language_target_enforcement
        )
        ref = PROVIDERS.program_api.get_language(language_id)
        return self.wrap_member(ref)

    def _list_languages(self):
        """List languages.

        GET/HEAD /v1/languages
        """
        filters = ('name', 'is_object_oriented', 'is_generic', 'is_static')
        target = None

        hints = self.build_driver_hints(filters)
        ENFORCER.enforce_call(
            action='xerox:list_languages',
            filters=filters,
            target_attr=target
        )
        refs = PROVIDERS.program_api.list_languages(hints=hints)

        return self.wrap_collection(refs, hints=hints)

    def post(self):
        """Create a language.

        POST /v1/languages
        """
        language_data = self.request_body_json.get('language', {})
        target = {'language': language_data}
        ENFORCER.enforce_call(
            action='xerox:create_language', target_attr=target
        )
        validation.lazy_validate(schema.language_create, language_data)
        language_data = self._normalize_dict(language_data)
        ref = PROVIDERS.program_api.create_language(
            language_data,
            initiator=self.audit_initiator)
        return self.wrap_member(ref), http_client.CREATED

    def delete(self, language_id=None):
        """Delete a language.

        DELETE /v1/language/{language_id}
        """
        ENFORCER.enforce_call(
            action='xerox:delete_language',
            build_target=_build_language_target_enforcement
        )
        PROVIDERS.program_api.delete_language(language_id)
        return None, http_client.NO_CONTENT


class LanguageAPI(x_flask.APIBase):
    _name = 'language'
    _import_name = __name__
    resources = [LanguageResource]
    resource_mapping = []


APIs = (LanguageAPI,)
