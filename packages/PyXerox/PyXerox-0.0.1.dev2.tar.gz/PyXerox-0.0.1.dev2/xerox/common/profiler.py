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
import osprofiler.initializer

import xerox.conf


CONF = xerox.conf.CONF
LOG = log.getLogger(__name__)


def setup(name, host='0.0.0.0'):  # nosec
    """Setup OSprofiler notifier and enable profiling.

    :param name: name of the service that will be profiled
    :param host: hostname or host IP address that the service will be
                 running on. By default host will be set to 0.0.0.0, but more
                 specified host name / address usage is highly recommended.
    """
    if CONF.profiler.enabled:
        osprofiler.initializer.init_from_conf(
            conf=CONF,
            context={},
            project="xerox",
            service=name,
            host=host
        )
        LOG.info("OSProfiler is enabled.\n"
                 "Traces provided from the profiler "
                 "can only be subscribed to using the same HMAC keys that "
                 "are configured in Xerox's configuration file "
                 "under the [profiler] section. \n To disable OSprofiler "
                 "set in /etc/xerox/xerox.conf:\n"
                 "[profiler]\n"
                 "enabled=false")
