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

"""A couple common constants for Auth data."""

# Header used to transmit the auth token
AUTH_TOKEN_HEADER = 'X-Auth-Token'  # nosec


# Header used to transmit the auth receipt
AUTH_RECEIPT_HEADER = 'Openstack-Auth-Receipt'


# Header used to transmit the subject token
SUBJECT_TOKEN_HEADER = 'X-Subject-Token'  # nosec

# Environment variable used to convey the Xerox auth context,
# the user credential used for policy enforcement.
AUTH_CONTEXT_ENV = 'XEROX_AUTH_CONTEXT'

# Header set by versions of keystonemiddleware that understand application
# credential access rules
ACCESS_RULES_HEADER = 'OpenStack-Identity-Access-Rules'
