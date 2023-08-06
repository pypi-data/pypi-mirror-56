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

# NOTE(morgan): Import relevant stuff so importing individual under-pinnings
# isn't needed, xerox.server.flask exposes all the interesting bits
# needed to develop restful APIs for xerox.

from xerox.server.flask.common import APIBase  # noqa
from xerox.server.flask.common import base_url  # noqa
from xerox.server.flask.common import construct_json_home_data  # noqa
from xerox.server.flask.common import construct_resource_map  # noqa
from xerox.server.flask.common import full_url  # noqa
from xerox.server.flask.common import JsonHomeData  # noqa
from xerox.server.flask.common import ResourceBase  # noqa
from xerox.server.flask.common import ResourceMap  # noqa
from xerox.server.flask.common import unenforced_api  # noqa


# NOTE(morgan): This allows for from xerox.flask import * and have all the
# cool stuff needed to develop new APIs within a module/subsystem
__all__ = ('APIBase', 'JsonHomeData', 'ResourceBase', 'ResourceMap',
           'base_url', 'construct_json_home_data',
           'construct_resource_map', 'full_url', 'unenforced_api')
