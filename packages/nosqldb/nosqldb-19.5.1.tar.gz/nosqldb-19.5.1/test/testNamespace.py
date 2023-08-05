#
#  This file is part of Oracle NoSQL Database
#  Copyright (C) 2014, 2018 Oracle and/or its affiliates.  All rights reserved.
#
# If you have received this file as part of Oracle NoSQL Database the
# following applies to the work as a whole:
#
#   Oracle NoSQL Database server software is free software: you can
#   redistribute it and/or modify it under the terms of the GNU Affero
#   General Public License as published by the Free Software Foundation,
#   version 3.
#
#   Oracle NoSQL Database is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Affero General Public License for more details.
#
# If you have received this file as part of Oracle NoSQL Database Client or
# distributed separately the following applies:
#
#   Oracle NoSQL Database client software is free software: you can
#   redistribute it and/or modify it under the terms of the Apache License
#   as published by the Apache Software Foundation, version 2.0.
#
# You should have received a copy of the GNU Affero General Public License
# and/or the Apache License in the LICENSE file along with Oracle NoSQL
# Database client or server distribution.  If not, see
# <http://www.gnu.org/licenses/>
# or
# <http://www.apache.org/licenses/LICENSE-2.0>.
#
# An active Oracle commercial licensing agreement for this product supersedes
# these licenses and in such case the license notices, but not the copyright
# notice, may be removed by you in connection with your distribution that is
# in accordance with the commercial licensing terms.
#
# For more information please contact:
#
# berkeleydb-info_us@oracle.com
#
import unittest

from nosqldb import COMMIT_NO_SYNC
from nosqldb import Factory
from nosqldb import IllegalArgumentException
from nosqldb import Row
from nosqldb import StoreConfig
from nosqldb import WriteOptions
from nosqldb import ONDB_DURABILITY
from nosqldb import ONDB_RETURN_CHOICE
from nosqldb import ONDB_TIMEOUT
from testSetup import add_runtime_params
from testSetup import get_kvproxy_config
from testSetup import get_kvstore_config
from testSetup import get_store
from testSetup import host_port
from testSetup import set_security


class TestNamespace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        namespace_name = 'ns'
        table_names = ['tbl', namespace_name + ':tbl']
        for t in table_names:
            cls._store.execute_sync("DROP TABLE IF EXISTS " + t)
        cls._store.execute_sync("DROP NAMESPACE IF EXISTS ns CASCADE")
        cls._store.refresh_tables()
        cls._store.execute_sync("CREATE NAMESPACE ns")
        cls._store.execute_sync("CREATE TABLE tbl (id INTEGER, " +
                                "name STRING, PRIMARY KEY (id))")
        cls._store.execute_sync("CREATE TABLE ns:tbl (id INTEGER, " +
                                "name STRING, PRIMARY KEY (id))")
        cls._store.refresh_tables()

    @classmethod
    def tearDownClass(cls):
        namespace_name = 'ns'
        table_names = ['tbl', namespace_name + ':tbl']
        for t in table_names:
            cls._store.execute_sync("DROP TABLE IF EXISTS " + t)
        cls._store.execute_sync("DROP NAMESPACE IF EXISTS ns CASCADE")
        cls._store.refresh_tables()
        cls._store.close()

    def setUp(self):
        s_conf = get_kvstore_config()
        p_conf = get_kvproxy_config()
        set_security(s_conf, p_conf)
        s_conf.set_durability({
            'master_sync': 'SYNC',
            'replica_sync': 'NO_SYNC',
            'replica_ack': 'ALL'})
        StoreConfig.change_log('DEBUG', None)
        self.store = Factory.open(host_port, s_conf, p_conf)
        self.writeopts = WriteOptions({ONDB_DURABILITY: COMMIT_NO_SYNC,
                                  ONDB_TIMEOUT: 5000,
                                  ONDB_RETURN_CHOICE: 'ALL'})

    def tearDown(self):
        self.store.close()

    def testNamespace(self):
        self.table = 'tbl'
        namestr = 'tbl'
        nstable = 'ns:tbl'
        id = 1
        self.row = Row({'id': id, 'name': namestr})
        version, oldrow = self.store.put(self.table, self.row)
        primary_key = {"id": id}
        readrow = self.store.get(self.table, primary_key)
        self.assertEqual(namestr, readrow['name'])
        emptyrow = self.store.get(nstable, primary_key)
        self.assertIsNone(emptyrow)

        id = 2
        namestr = nstable
        self.row = Row({'id': id, 'name': namestr})
        version, oldrow = self.store.put(nstable, self.row)
        primary_key = {"id": id}
        readrow = self.store.get(nstable, primary_key)
        self.assertEqual(namestr, readrow['name'])
        emptyrow = self.store.get(self.table, primary_key)
        self.assertIsNone(emptyrow)

        self._store.execute_sync("CREATE INDEX idx on tbl(name)")
        self._store.execute_sync("CREATE INDEX idx on ns:tbl(name)")

    def testCreateDropNamespace(self):
        namespace_names = ['ns1', 'ns.n2']
        for t in namespace_names:
            self._store.execute_sync("DROP NAMESPACE IF EXISTS " + t +
                                     " CASCADE")
        self._store.refresh_tables()
        for t in namespace_names:
            self._store.execute_sync("CREATE NAMESPACE " + t)
            self._store.execute_sync("CREATE NAMESPACE IF NOT EXISTS " + t)
        self._store.execute_sync("DROP NAMESPACE ns.n2")

        self._store.execute_sync("CREATE TABLE ns1:t1 (id INTEGER, " +
                                "name STRING, PRIMARY KEY (id))")
        self.assertRaises(IllegalArgumentException,
                          self._store.execute_sync,
                          "DROP NAMESPACE ns1")
        self._store.execute_sync("DROP TABLE ns1:t1")
        self._store.execute_sync("DROP NAMESPACE ns1")

        invalid_namespace_names = ["", " ", "9Ns", "Ns.003", "Ns$name",
                                   "Ns:name", "Ns@name", "Ns-name", "_NsName",
                                   "sysname", "sysdefault"]
        for t in invalid_namespace_names:
            self.assertRaises(IllegalArgumentException,
                              self._store.execute_sync,
                              "CREATE NAMESPACE " + t)

        system_namespace_names = ["sysdefault", "SYSdefault", "sys001"]
        for t in system_namespace_names:
            self.assertRaises(IllegalArgumentException,
                              self._store.execute_sync,
                              "DROP NAMESPACE " + t)

if __name__ == '__main__':
    add_runtime_params()
    unittest.main()