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

from oslo_context import context as oslo_context


REQUEST_CONTEXT_ENV = 'xerox.oslo_request_context'


def _prop(name):
    return property(lambda x: getattr(x, name),
                    lambda x, y: setattr(x, name, y))


class RequestContext(oslo_context.RequestContext):

    def __init__(self, **kwargs):
        self.username = kwargs.pop('username', None)
        self.project_tag_name = kwargs.pop('project_tag_name', None)

        self.is_delegated_auth = kwargs.pop('is_delegated_auth', False)

        self.authenticated = kwargs.pop('authenticated', False)
        super(RequestContext, self).__init__(**kwargs)

    def to_policy_values(self):
        """Add xerox-specific policy values to policy representation.

        This method converts generic policy values to a dictionary form using
        the base implementation from oslo_context.context.RequestContext.
        Afterwards, it is going to pull xerox-specific values off the
        context and represent them as items in the policy values dictionary.
        This is because xerox uses default policies that rely on these
        values, so we need to guarantee they are present during policy
        enforcement if they are present on the context object.

        This method is automatically called in
        oslo_policy.policy.Enforcer.enforce() if oslo.policy knows it's dealing
        with a context object.

        """
        # TODO(morgan): Rework this to not need an explicit token render as
        # this is a generally poorly designed behavior. The enforcer should not
        # rely on a contract of the token's rendered JSON form. This likely
        # needs reworking of how we handle the context in oslo.policy. Until
        # this is reworked, it is not possible to merge the token render
        # function into xerox.api
        values = super(RequestContext, self).to_policy_values()
        values['project_id'] = self.project_id if self.project_id else None
        return values
