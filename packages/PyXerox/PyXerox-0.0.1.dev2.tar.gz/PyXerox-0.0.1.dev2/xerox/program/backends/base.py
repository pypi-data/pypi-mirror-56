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

import abc

import six

from xerox import exception


@six.add_metaclass(abc.ABCMeta)
class ProgramDriverBase(object):

    @abc.abstractmethod
    def create_language(self, language):
        """Create a new language.

        :param dict language: Language data

        :returns: a new language
        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def update_language(self, language_id, language):
        """Update an existing language.

        :param str language_id: Language ID.
        :param dict language: Language modification. See language schema in
            :class:`~.ProgramDriverBase`. Properties set to None will be
            removed. Required properties cannot be removed.

        :returns: language.
            See language schema in :class:`~.ProgramDriverBase`.

        :raises xerox.exception.LanguageNotFound: If the user doesn't exist.
        :raises xerox.exception.Conflict: If a duplicate language exists in the
            database.

        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def get_language(self, language_id):
        """Get an language by the language id.

        :param str language_id: Language ID
        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def list_languages(self, hints):
        """List languages.

        :param str language_id: Language ID
        :param hints: contains the list of filters yet to be satisfied.
                      Any filters satisfied here will be removed so that
                      the caller will know if any filters remain.
        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def delete_language(self, language_id):
        """Delete a single language.

        :param str language_id: ID of the language
            to delete.

        """
        raise exception.NotImplemented()  # pragma: no cover
