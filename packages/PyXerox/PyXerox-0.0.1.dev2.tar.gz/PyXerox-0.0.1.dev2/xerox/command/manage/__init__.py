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

from oslo_config import cfg
from oslo_log import log
import pbr.version

from xerox.command.manage import db_sync
from xerox.command.manage import db_version
from xerox.common import sql
import xerox.conf

CONF = xerox.conf.CONF
LOG = log.getLogger(__name__)


CMDS = [
    db_sync,
    db_version,
]


def add_command_parsers(subparsers):
    for cmd in CMDS:
        cmd.CMD.add_argument_parser(subparsers)


command_opt = cfg.SubCommandOpt('command',
                                title='Commands',
                                help='Available commands',
                                handler=add_command_parsers)


def main(argv=None, developer_config_file=None):
    """Main entry point into the xerox-manage CLI utility.

    :param argv: Arguments supplied via the command line using the ``sys``
                 standard library.
    :type argv: list
    :param developer_config_file: The location of a configuration file normally
                                  found in development environments.
    :type developer_config_file: string

    """
    CONF.register_cli_opt(command_opt)

    xerox.conf.configure()
    sql.initialize()
    xerox.conf.set_default_for_default_log_levels()

    user_supplied_config_file = False
    if argv:
        for argument in argv:
            if argument == '--config-file':
                user_supplied_config_file = True

    if developer_config_file:
        developer_config_file = [developer_config_file]

    # NOTE(lbragstad): At this point in processing, the first element of argv
    # is the binary location of xerox-manage, which oslo.config doesn't need
    # and is xerox specific. Only pass a list of arguments so that
    # oslo.config can determine configuration file locations based on user
    # provided arguments, if present.
    CONF(args=argv[1:],
         project='xerox',
         version=pbr.version.VersionInfo('xerox').version_string(),
         usage='%(prog)s [' + '|'.join([cmd.CMD.name for cmd in CMDS]) + ']',
         default_config_files=developer_config_file)

    if not CONF.default_config_files and not user_supplied_config_file:
        LOG.warning('Config file not found, using default configs.')
    xerox.conf.setup_logging()
    CONF.command.cmd_class.main()
