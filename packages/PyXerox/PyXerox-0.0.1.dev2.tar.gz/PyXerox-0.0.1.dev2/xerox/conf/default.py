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

from xerox.conf import utils


admin_token = cfg.StrOpt(
    'admin_token',
    secret=True,
    help=utils.fmt("""
Using this feature is *NOT* recommended. Instead, use the `xerox-manage
bootstrap` command. The value of this option is treated as a "shared secret"
that can be used to bootstrap Xerox through the API. This "token" does not
represent a user (it has no identity), and carries no explicit authorization
(it effectively bypasses most authorization checks). If set to `None`, the
value is ignored and the `admin_token` middleware is effectively disabled.
"""))

public_endpoint = cfg.URIOpt(
    'public_endpoint',
    help=utils.fmt("""
The base public endpoint URL for Xerox that is advertised to clients (NOTE:
this does NOT affect how Xerox listens for connections). Defaults to the
base host URL of the request. For example, if xerox receives a request to
`http://server:5000/v3/users`, then this will option will be automatically
treated as `http://server:5000`. You should only need to set option if either
the value of the base URL contains a path that xerox does not automatically
infer (`/prefix/v3`), or if the endpoint should be found on a different host.
"""))

max_project_tree_depth = cfg.IntOpt(
    'max_project_tree_depth',
    default=5,
    help=utils.fmt("""
Maximum depth of the project hierarchy, excluding the project acting as a
domain at the top of the hierarchy. WARNING: Setting it to a large value may
adversely impact performance.
"""))

max_param_size = cfg.IntOpt(
    'max_param_size',
    default=64,
    help=utils.fmt("""
Limit the sizes of user & project ID/names.
"""))

# NOTE(breton): 255 is the size of the database columns used for ID fields.
# This size is picked so that the tokens can be indexed in-place as opposed to
# being entries in a string table. Thus, this is a performance decision.
max_token_size = cfg.IntOpt(
    'max_token_size',
    default=255,
    help=utils.fmt("""
Similar to `[DEFAULT] max_param_size`, but provides an exception for token
values. With Fernet tokens, this can be set as low as 255. With UUID tokens,
this should be set to 32).
"""))

list_limit = cfg.IntOpt(
    'list_limit',
    help=utils.fmt("""
The maximum number of entities that will be returned in a collection. This
global limit may be then overridden for a specific driver, by specifying a
list_limit in the appropriate section (for example, `[assignment]`). No limit
is set by default. In larger deployments, it is recommended that you set this
to a reasonable number to prevent operations like listing all users and
projects from placing an unnecessary load on the system.
"""))

strict_password_check = cfg.BoolOpt(
    'strict_password_check',
    default=False,
    help=utils.fmt("""
If set to true, strict password length checking is performed for password
manipulation. If a password exceeds the maximum length, the operation will fail
with an HTTP 403 Forbidden error. If set to false, passwords are automatically
truncated to the maximum length.
"""))

insecure_debug = cfg.BoolOpt(
    'insecure_debug',
    default=False,
    help=utils.fmt("""
If set to true, then the server will return information in HTTP responses that
may allow an unauthenticated or authenticated user to get more information than
normal, such as additional details about why authentication failed. This may be
useful for debugging but is insecure.
"""))

default_publisher_id = cfg.StrOpt(
    'default_publisher_id',
    help=utils.fmt("""
Default `publisher_id` for outgoing notifications. If left undefined, Xerox
will default to using the server's host name.
"""))

notification_format = cfg.StrOpt(
    'notification_format',
    default='cadf',
    choices=['basic', 'cadf'],
    help=utils.fmt("""
Define the notification format for identity service events. A `basic`
notification only has information about the resource being operated on. A
`cadf` notification has the same information, as well as information about the
initiator of the event. The `cadf` option is entirely backwards compatible with
the `basic` option, but is fully CADF-compliant, and is recommended for
auditing use cases.
"""))

notification_opt_out = cfg.MultiStrOpt(
    'notification_opt_out',
    default=["identity.authenticate.success",
             "identity.authenticate.pending",
             "identity.authenticate.failed"],
    help=utils.fmt("""
You can reduce the number of notifications xerox emits by explicitly
opting out. Xerox will not emit notifications that match the patterns
expressed in this list. Values are expected to be in the form of
`identity.<resource_type>.<operation>`. By default, all notifications
related to authentication are automatically suppressed. This field can be
set multiple times in order to opt-out of multiple notification topics. For
example, the following suppresses notifications describing user creation or
successful authentication events:
notification_opt_out=identity.user.create
notification_opt_out=identity.authenticate.success
"""))


GROUP_NAME = 'DEFAULT'
ALL_OPTS = [
    admin_token,
    public_endpoint,
    max_project_tree_depth,
    max_param_size,
    max_token_size,
    list_limit,
    strict_password_check,
    insecure_debug,
    default_publisher_id,
    notification_format,
    notification_opt_out,
]


def register_opts(conf):
    conf.register_opts(ALL_OPTS)


def list_opts():
    return {GROUP_NAME: ALL_OPTS}
