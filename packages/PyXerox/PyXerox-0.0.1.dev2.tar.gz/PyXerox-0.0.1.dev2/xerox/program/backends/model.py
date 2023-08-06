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

from xerox.common import sql


class Language(sql.ModelBase, sql.ModelDictMixinWithExtras):
    __tablename__ = 'language'
    attributes = ['id', 'name', 'is_object_oriented', 'is_generic',
                  'is_static']
    readonly_attributes = ['id']

    id = sql.Column(sql.String(64), primary_key=True)
    name = sql.Column(sql.String(64), unique=True, nullable=False, index=True)
    is_object_oriented = sql.Column(sql.Boolean)
    is_generic = sql.Column(sql.Boolean)
    is_static = sql.Column(sql.Boolean)
    extra = sql.Column(sql.JsonBlob())
