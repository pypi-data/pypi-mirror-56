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

import sys

import migrate
from oslo_db.sqlalchemy import migration
from oslo_log import log

from xerox.command import base
from xerox.common.sql import upgrades
import xerox.conf

CONF = xerox.conf.CONF
LOG = log.getLogger(__name__)


class DbSync(base.BaseApp):
    """Sync the database."""

    name = 'db_sync'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(DbSync, cls).add_argument_parser(subparsers)
        parser.add_argument('version', default=None, nargs='?',
                            help=('Migrate the database up to a specified '
                                  'version. If not provided, db_sync will '
                                  'migrate the database to the latest known '
                                  'version. Schema downgrades are not '
                                  'supported.'))
        parser.add_argument('--extension', default=None,
                            help=('This is a deprecated option to migrate a '
                                  'specified extension. Since extensions are '
                                  'now part of the main repository, '
                                  'specifying db_sync without this option '
                                  'will cause all extensions to be migrated.'))
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--expand', default=False, action='store_true',
                           help=('Expand the database schema in preparation '
                                 'for data migration.'))
        group.add_argument('--migrate', default=False,
                           action='store_true',
                           help=('Copy all data that needs to be migrated '
                                 'within the database ahead of starting the '
                                 'first xerox node upgraded to the new '
                                 'release. This command should be run '
                                 'after the --expand command. Once the '
                                 '--migrate command has completed, you can '
                                 'upgrade all your xerox nodes to the new '
                                 'release and restart them.'))

        group.add_argument('--contract', default=False, action='store_true',
                           help=('Remove any database tables and columns '
                                 'that are no longer required. This command '
                                 'should be run after all xerox nodes are '
                                 'running the new release.'))

        group.add_argument('--check', default=False, action='store_true',
                           help=('Check for outstanding database actions that '
                                 'still need to be executed. This command can '
                                 'be used to verify the condition of the '
                                 'current database state.'))
        return parser

    @classmethod
    def check_db_sync_status(cls):
        status = 0
        try:
            expand_version = upgrades.get_db_version(repo='expand_repo')
        except migration.exception.DBMigrationError:
            LOG.info('Your database is not currently under version '
                     'control or the database is already controlled. Your '
                     'first step is to run `xerox-manage db_sync '
                     '--expand`.')
            return 2
        try:
            migrate_version = upgrades.get_db_version(
                repo='data_migration_repo')
        except migration.exception.DBMigrationError:
            migrate_version = 0
        try:
            contract_version = upgrades.get_db_version(repo='contract_repo')
        except migration.exception.DBMigrationError:
            contract_version = 0

        repo = migrate.versioning.repository.Repository(
            upgrades.find_repo('expand_repo'))
        migration_script_version = int(max(repo.versions.versions))

        if (contract_version > migrate_version or migrate_version >
                expand_version):
            LOG.info('Your database is out of sync. For more information '
                     'refer to https://docs.openstack.org/xerox/'
                     'latest/admin/identity-upgrading.html')
            status = 1
        elif migration_script_version > expand_version:
            LOG.info('Your database is not up to date. Your first step is '
                     'to run `xerox-manage db_sync --expand`.')
            status = 2
        elif expand_version > migrate_version:
            LOG.info('Expand version is ahead of migrate. Your next step '
                     'is to run `xerox-manage db_sync --migrate`.')
            status = 3
        elif migrate_version > contract_version:
            LOG.info('Migrate version is ahead of contract. Your next '
                     'step is to run `xerox-manage db_sync --contract`.')
            status = 4
        elif (migration_script_version == expand_version == migrate_version ==
                contract_version):
            LOG.info('All db_sync commands are upgraded to the same '
                     'version and up-to-date.')
        LOG.info('The latest installed migration script version is: '
                 '%(script)d.\nCurrent repository versions:\nExpand: '
                 '%(expand)d \nMigrate: %(migrate)d\nContract: '
                 '%(contract)d', {'script': migration_script_version,
                                  'expand': expand_version,
                                  'migrate': migrate_version,
                                  'contract': contract_version})
        return status

    @staticmethod
    def main():
        base.assert_not_extension(CONF.command.extension)
        # It is possible to run expand and migrate at the same time,
        # expand needs to run first however.
        if CONF.command.check:
            sys.exit(DbSync.check_db_sync_status())
        elif CONF.command.expand and CONF.command.migrate:
            upgrades.expand_schema()
            upgrades.migrate_data()
        elif CONF.command.expand:
            upgrades.expand_schema()
        elif CONF.command.migrate:
            upgrades.migrate_data()
        elif CONF.command.contract:
            upgrades.contract_schema()
        else:
            upgrades.offline_sync_database_to_version(
                CONF.command.version)


CMD = DbSync
