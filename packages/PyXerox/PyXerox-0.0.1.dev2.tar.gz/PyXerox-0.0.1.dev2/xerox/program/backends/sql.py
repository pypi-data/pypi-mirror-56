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

from oslo_db import api as oslo_db_api

from xerox.common import driver_hints
from xerox.common import sql
from xerox import exception
from xerox.program.backends import base
from xerox.program.backends import model


class Program(base.ProgramDriverBase):

    # language crud

    @sql.handle_conflicts(conflict_type='language')
    def create_language(self, language_id, language):
        with sql.session_for_write() as session:
            language_ref = model.Language.from_dict(language)
            session.add(language_ref)
            return language_ref.to_dict()

    @sql.handle_conflicts(conflict_type='language')
    def update_language(self, language_id, language):
        with sql.session_for_write() as session:
            language_ref = self._get_language(session, language_id)
            old_language_dict = language_ref.to_dict()
            for k in language:
                old_language_dict[k] = language[k]
            new_language = model.Language.from_dict(old_language_dict)
            for attr in model.Language.attributes:
                # NOTE(muxin): We can not update language's extra column.
                if attr not in model.Language.readonly_attributes:
                    setattr(language_ref, attr, getattr(new_language, attr))
        return language_ref.to_dict()

    def get_language(self, language_id):
        with sql.session_for_read() as session:
            return self._get_language(session, language_id).to_dict()

    def _get_language(self, session, language_id):
        language_ref = session.query(model.Language).get(language_id)
        if not language_ref:
            raise exception.LanguageNotFound(language_id=language_id)
        return language_ref

    @driver_hints.truncated
    def list_languages(self, hints=None):
        with sql.session_for_read() as session:
            query = session.query(model.Language)
            language_refs = sql.filter_limit_query(model.Language,
                                                   query,
                                                   hints)
            return [x.to_dict() for x in language_refs]

    @oslo_db_api.wrap_db_retry(retry_on_deadlock=True)
    def delete_language(self, language_id):
        with sql.session_for_write() as session:
            ref = self._get_language(session, language_id)
            session.delete(ref)
