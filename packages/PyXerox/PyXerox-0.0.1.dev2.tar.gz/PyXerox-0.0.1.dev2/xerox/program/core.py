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

import uuid

from oslo_log import log

from xerox.common import cache
from xerox.common import driver_hints
from xerox.common import manager
from xerox.common import provider_api
import xerox.conf


CONF = xerox.conf.CONF

LOG = log.getLogger(__name__)

PROVIDERS = provider_api.ProviderAPIs

MEMOIZE = cache.get_memoization_decorator(group='program')


class Manager(manager.Manager):
    """Default pivot point for the Program backend.

    See :mod:`xerox.common.manager.Manager` for more details on how this
    dynamically calls the backend.

    """

    driver_namespace = 'xerox.program'
    _provides_api = 'program_api'

    _LANGUAGE = 'language'

    def __init__(self):
        super(Manager, self).__init__(CONF.program.driver)

    def get_language(self, language_id):
        """Get language details.

        :param str language_id: Language ID

        :returns: a language detail
        """
        return self.driver.get_language(language_id)

    def list_languages(self, hints=None):
        """List languages.

        :param dict hints: Properties to filter on

        :returns: a list of languages
        """
        hints = hints or driver_hints.Hints()
        return self.driver.list_languages(hints)

    def create_language(self, language_ref, initiator=None):
        """Create a new language.

        :param dict language_ref: Language data
        :param initiator: CADF initiator

        :returns: a new language
        """
        language = language_ref.copy()
        language['name'] = language['name'].strip()
        language['id'] = uuid.uuid4().hex
        ref = self.driver.create_language(language['id'], language)
        return ref

    def update_language(self, language_id, language_ref, initiator=None):
        """Update an exist language.

        :param str language_id: Language ID
        :param dict language_ref: Language data
        :param initiator: CADF initiator

        :raises xerox.exception.LanguageNotFound: If the language doesn't
            exists.

        :returns: an updated language
        """
        ref = self.driver.update_language(language_id, language_ref)
        return ref

    def delete_language(self, language_id, initiator=None):
        """Delete a language.

        :param str language_id: Language ID
        :param initiator: CADF initiator

        :raises xerox.exception.LanguageNotFound: If the language doesn't
            exists.
        """
        self.driver.delete_language(language_id)
