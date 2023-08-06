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

# NOTE(morgan): This entire module is to provide compatibility for the old
# @protected style decorator enforcement. All new enforcement should directly
# reference the Enforcer object itself.
from xerox.common.rbac_enforcer import enforcer
from xerox import conf


CONF = conf.CONF


# NOTE(morgan): Shared-state enforcer object
_ENFORCER = enforcer.RBACEnforcer()


def reset():
    _ENFORCER._reset()


def get_enforcer():
    """Entrypoint that must return the raw oslo.policy enforcer obj.

    This is utilized by the command-line policy tools.

    :returns: :class:`oslo_policy.policy.Enforcer`
    """
    # Here we pass an empty list of arguments because there aren't any
    # arguments that oslo.config or oslo.policy shouldn't already understand
    # from the CONF object. This makes things easier here because we don't have
    # to parse arguments passed in from the command line and remove unexpected
    # arguments before building a Config object.
    CONF([], project='xerox')
    return _ENFORCER._enforcer


enforce = _ENFORCER._enforce
