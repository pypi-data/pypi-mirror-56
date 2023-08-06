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

from xerox.command import base
from xerox.common.sql import upgrades
import xerox.conf

CONF = xerox.conf.CONF


class DbVersion(base.BaseApp):
    """Print the current migration version of the database."""

    name = 'db_version'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(DbVersion, cls).add_argument_parser(subparsers)
        parser.add_argument('--extension', default=None,
                            help=('This is a deprecated option to print the '
                                  'version of a specified extension. Since '
                                  'extensions are now part of the main '
                                  'repository, the version of an extension is '
                                  'implicit in the version of the main '
                                  'repository.'))

    @staticmethod
    def main():
        base.assert_not_extension(CONF.command.extension)
        print(upgrades.get_db_version())


CMD = DbVersion
