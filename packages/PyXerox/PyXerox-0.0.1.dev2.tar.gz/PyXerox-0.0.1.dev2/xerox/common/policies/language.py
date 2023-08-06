# Copyright 2019 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_policy import policy

from xerox.common.policies import base

collection_path = '/v3/languages'
resource_path = collection_path + '/{language_id}'

SYSTEM_READER_OR_OWNER = (
    '(' + base.SYSTEM_READER + ') or '
    'user_id:%(target.user.id)s'
)

SYSTEM_ADMIN_OR_OWNER = (
    '(' + base.SYSTEM_ADMIN + ') or '
    'user_id:%(target.user.id)s'
)

language_policies = [
    policy.DocumentedRuleDefault(
        name=base.XEROX % 'get_language',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system', 'project'],
        description='Show language details.',
        operations=[{'path': resource_path,
                     'method': 'GET'},
                    {'path': resource_path,
                     'method': 'HEAD'}]),
    policy.DocumentedRuleDefault(
        name=base.XEROX % 'list_languages',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system', 'project'],
        description='List languages.',
        operations=[{'path': collection_path,
                     'method': 'GET'},
                    {'path': collection_path,
                     'method': 'HEAD'}]),
    policy.DocumentedRuleDefault(
        name=base.XEROX % 'create_language',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system', 'project'],
        description='Create languages.',
        operations=[{'path': resource_path,
                     'method': 'POST'}]),
    policy.DocumentedRuleDefault(
        name=base.XEROX % 'delete_language',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system', 'project'],
        description='Delete a language.',
        operations=[{'path': resource_path,
                     'method': 'DELETE'}])
]


def list_rules():
    return language_policies
