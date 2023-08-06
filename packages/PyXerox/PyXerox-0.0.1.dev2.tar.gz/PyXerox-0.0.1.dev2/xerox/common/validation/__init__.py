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
"""Request body validating middleware for OpenStack Identity resources."""

from xerox.common.validation import validators


def lazy_validate(request_body_schema, resource_to_validate):
    """A non-decorator way to validate a request, to be used inline.

    :param request_body_schema: a schema to validate the resource reference
    :param resource_to_validate: dictionary to validate
    :raises xerox.exception.ValidationError: if `resource_to_validate` is
            None. (see wrapper method below).
    :raises TypeError: at decoration time when the expected resource to
                       validate isn't found in the decorated method's
                       signature

    """
    schema_validator = validators.SchemaValidator(request_body_schema)
    schema_validator.validate(resource_to_validate)


def nullable(property_schema):
    """Clone a property schema into one that is nullable.

    :param dict property_schema: schema to clone into a nullable schema
    :returns: a new dict schema
    """
    # TODO(dstanek): deal with the case where type is already a list; we don't
    #                do that yet so I'm not wasting time on it
    new_schema = property_schema.copy()
    new_schema['type'] = [property_schema['type'], 'null']
    # NOTE(kmalloc): If enum is specified (such as our boolean case) ensure we
    # add null to the enum as well so that null can be passed/validated as
    # expected. Without adding to the enum, null will not validate as enum is
    # explicitly listing valid values. According to the JSON Schema
    # specification, the values must be unique in the enum array.
    if 'enum' in new_schema and None not in new_schema['enum']:
        # In the enum the 'null' is NoneType
        new_schema['enum'].append(None)
    return new_schema
