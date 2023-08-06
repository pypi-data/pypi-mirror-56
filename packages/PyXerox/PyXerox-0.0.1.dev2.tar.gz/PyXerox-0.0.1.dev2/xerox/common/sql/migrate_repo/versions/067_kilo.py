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

import migrate
from oslo_log import log
import sqlalchemy as sql

from xerox.common import sql as ks_sql


LOG = log.getLogger(__name__)


def upgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    if migrate_engine.name == 'mysql':
        # In Folsom we explicitly converted migrate_version to UTF8.
        migrate_engine.execute(
            'ALTER TABLE migrate_version CONVERT TO CHARACTER SET utf8')
        # Set default DB charset to UTF8.
        migrate_engine.execute(
            'ALTER DATABASE %s DEFAULT CHARACTER SET utf8' %
            migrate_engine.url.database)

    language = sql.Table(
        'language', meta,
        sql.Column('id', sql.String(length=64), primary_key=True),
        sql.Column('name', sql.String(length=64), unique=True, nullable=False),
        sql.Column('is_object_oriented', sql.Boolean, default=False,
                   nullable=False),
        sql.Column('is_generic', sql.Boolean, default=False, nullable=False),
        sql.Column('is_static', sql.Boolean, default=True, nullable=False),
        sql.Column('extra', ks_sql.JsonBlob.impl),
        mysql_engine='InnoDB',
        mysql_charset='utf8')

    # create all tables
    tables = [language]

    for table in tables:
        try:
            table.create()
        except Exception:
            LOG.exception('Exception while creating table: %r', table)
            raise

    # Unique Constraints

    # Indexes
    sql.Index('ix_language_name', language.c.name).create()

    fkeys = []

    for fkey in fkeys:
        migrate.ForeignKeyConstraint(columns=fkey['columns'],
                                     refcolumns=fkey['references'],
                                     name=fkey.get('name')).create()
