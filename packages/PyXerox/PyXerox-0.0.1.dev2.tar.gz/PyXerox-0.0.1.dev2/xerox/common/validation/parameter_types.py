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
"""Common parameter types for validating a request reference."""

boolean = {
    'type': 'boolean',
    'enum': [True, False]
}

# NOTE(lbragstad): Be mindful of this pattern as it might require changes
# once this is used on user names, LDAP-based user names specifically since
# commas aren't allowed in the following pattern. Here we are only going to
# check the length of the name and ensure that it's a string. Right now we are
# not going to validate on a naming pattern for issues with
# internationalization.
name = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 255,
    'pattern': '[\S]+'
}

external_id_string = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 64
}

id_string = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 64,
    # TODO(lbragstad): Find a way to make this configurable such that the end
    # user chooses how much control they want over id_strings with a regex
    'pattern': '^[a-zA-Z0-9-]+$'
}

mapping_id_string = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 64,
    'pattern': '^[a-zA-Z0-9-_]+$'
}

description = {
    'type': 'string'
}

url = {
    'type': 'string',
    'minLength': 0,
    'maxLength': 225,
    # NOTE(edmondsw): we could do more to validate per various RFCs, but
    # decision was made to err on the side of leniency. The following is based
    # on rfc1738 section 2.1
    'pattern': '^[a-zA-Z0-9+.-]+:.+'
}

email = {
    'type': 'string',
    'format': 'email'
}
