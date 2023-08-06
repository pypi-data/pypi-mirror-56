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

from xerox.common import sql
import xerox.conf
from xerox.server import backends


CONF = xerox.conf.CONF
LOG = log.getLogger(__name__)


def configure(version=None, config_files=None,
              pre_setup_logging_fn=lambda: None):
    xerox.conf.configure()
    sql.initialize()
    xerox.conf.set_config_defaults()

    CONF(project='xerox', version=version,
         default_config_files=config_files)

    pre_setup_logging_fn()
    xerox.conf.setup_logging()

    if CONF.insecure_debug:
        LOG.warning(
            'insecure_debug is enabled so responses may include sensitive '
            'information.')


def setup_backends(load_extra_backends_fn=lambda: {},
                   startup_application_fn=lambda: None):
    drivers = backends.load_backends()
    drivers.update(load_extra_backends_fn())
    res = startup_application_fn()
    return drivers, res
