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
from time import time
import unittest

from nosqldb import Factory
from nosqldb import IllegalArgumentException
from nosqldb import Operation
from nosqldb import OperationType
from nosqldb import Row
from nosqldb import StoreConfig
from nosqldb import TimeToLive
from nosqldb import WriteOptions
from nosqldb import ONDB_ABORT_IF_UNSUCCESSFUL
from nosqldb import ONDB_DELETE
from nosqldb import ONDB_DELETE_IF_VERSION
from nosqldb import ONDB_HOURS
from nosqldb import ONDB_OPERATION
from nosqldb import ONDB_OPERATION_TYPE
from nosqldb import ONDB_PUT
from nosqldb import ONDB_PUT_IF_ABSENT
from nosqldb import ONDB_PUT_IF_PRESENT
from nosqldb import ONDB_PUT_IF_VERSION
from nosqldb import ONDB_ROW
from nosqldb import ONDB_TABLE_NAME
from nosqldb import ONDB_TIMEUNIT
from nosqldb import ONDB_TTL_TIMEUNIT
from nosqldb import ONDB_TTL_VALUE
from nosqldb import ONDB_UPDATE_TTL
from nosqldb import ONDB_VERSION
from nosqldb import ONDB_WAS_SUCCESSFUL
from testSetup import add_runtime_params
from testSetup import get_kvproxy_config
from testSetup import get_kvstore_config
from testSetup import get_store
from testSetup import host_port
from testSetup import set_security
from testSetup import table_name


class TestExecuteBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        cls._table = table_name + "TableTest"
        cls._store.execute_sync('DROP TABLE IF EXISTS ' + cls._table)
        cls._store.execute_sync('CREATE TABLE IF NOT EXISTS ' + cls._table +
            ' ( id INTEGER, shardkey INTEGER, name STRING, age FLOAT, ' +
            ' PRIMARY KEY (SHARD(shardkey), id))')
        cls._store.refresh_tables()

    @classmethod
    def tearDownClass(cls):
        cls._store.execute_sync('DROP TABLE IF EXISTS ' + cls._table)
        cls._store.refresh_tables()
        cls._store.close()

    def setUp(self):
        self.table = table_name
        s_conf = get_kvstore_config()
        p_conf = get_kvproxy_config()
        set_security(s_conf, p_conf)
        StoreConfig.change_log("DEBUG", None)
        self.store = Factory.open(host_port, s_conf, p_conf)

    def tearDown(self):
        self.store.close()

    def testExecuteBatchPut(self):
        batch = [Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 0, 'name': 'John', 'age': 25,
                      'shardkey': 0}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 1, 'name': 'Chris', 'age': 30,
                      'shardkey': 0}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 2, 'name': 'Rick', 'age': 31,
                      'shardkey': 0}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 })]
        res = self.store.execute_updates(batch)
        self.store.multi_delete(self.table + "TableTest",
            Row({'shardkey': 0}))
        self.assertEqual(len(res), 3)

    def testExecuteBatchPutIfAbsent(self):
        batch = [Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_ABSENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 0, 'name': 'John', 'age': 25,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_ABSENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 1, 'name': 'Chris', 'age': 30,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 })]
        res = self.store.execute_updates(batch)
        row = Row({'shardkey': 1})
        res2 = self.store.multi_get(self.table + "TableTest", row, False)
        all_ok = True
        for r in res2:
            if (r['id'] == 0):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'John'):
                    all_ok = False
                    break
                if (r['age'] != 25):
                    all_ok = False
                    break
            if (r['id'] == 1):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'Chris'):
                    all_ok = False
                    break
                if (r['age'] != 30):
                    all_ok = False
                    break
        self.store.multi_delete(self.table + "TableTest",
            Row({'shardkey': 1}))
        self.assertTrue(all_ok)
        self.assertEqual(len(res), 2)

    def testExecuteBatchPutIfPresent(self):
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 0, 'shardKey': 1, 'name': 'A', 'age': 10}))
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 1, 'shardKey': 1, 'name': 'B', 'age': 20}))
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 2, 'shardKey': 1, 'name': 'C', 'age': 30}))
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 3, 'shardKey': 1, 'name': 'D', 'age': 40}))
        batch = [Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_PRESENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 0, 'name': 'John', 'age': 25,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_PRESENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 1, 'name': 'Chris', 'age': 30,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_PRESENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 2, 'name': 'Rick', 'age': 31,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_PRESENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 3, 'name': 'Marv', 'age': 34,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 })]
        res = self.store.execute_updates(batch)
        row = Row({'shardkey': 1})
        res2 = self.store.multi_get(self.table + "TableTest", row, False)
        all_ok = True
        for r in res2:
            if (r['id'] == 0):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'John'):
                    all_ok = False
                    break
                if (r['age'] != 25):
                    all_ok = False
                    break
            if (r['id'] == 1):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'Chris'):
                    all_ok = False
                    break
                if (r['age'] != 30):
                    all_ok = False
                    break
            if (r['id'] == 2):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'Rick'):
                    all_ok = False
                    break
                if (r['age'] != 31):
                    all_ok = False
                    break
            if (r['id'] == 3):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'Marv'):
                    all_ok = False
                    break
                if (r['age'] != 34):
                    all_ok = False
                    break
        self.store.multi_delete(self.table + "TableTest",
            Row({'shardkey': 1}))
        self.assertTrue(all_ok)
        self.assertEqual(len(res), 4)

    def testExecuteBatchPutIfVersion(self):
        versions = []
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 0, 'shardKey': 1, 'name': 'A', 'age': 10}))
        versions.append(v)
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 1, 'shardKey': 1, 'name': 'B', 'age': 20}))
        versions.append(v)
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 2, 'shardKey': 1, 'name': 'C', 'age': 30}))
        versions.append(v)
        batch = [Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_VERSION}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 0, 'name': 'John', 'age': 25,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True,
                  ONDB_VERSION: versions[0]
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_VERSION}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 1, 'name': 'Chris', 'age': 30,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True,
                  ONDB_VERSION: versions[1]
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_VERSION}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 2, 'name': 'Rick', 'age': 31,
                      'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True,
                  ONDB_VERSION: versions[2]
                 })]
        res = self.store.execute_updates(batch)
        row = Row({'shardkey': 1})
        res2 = self.store.multi_get(self.table + "TableTest", row, False)
        all_ok = True
        for r in res2:
            if (r['id'] == 0):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'John'):
                    all_ok = False
                    break
                if (r['age'] != 25):
                    all_ok = False
                    break
            if (r['id'] == 1):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'Chris'):
                    all_ok = False
                    break
                if (r['age'] != 30):
                    all_ok = False
                    break
            if (r['id'] == 2):
                if (r['shardkey'] != 1):
                    all_ok = False
                    break
                if (r['name'] != 'Rick'):
                    all_ok = False
                    break
                if (r['age'] != 31):
                    all_ok = False
                    break
        self.store.multi_delete(self.table + "TableTest",
            Row({'shardkey': 1}))
        self.assertTrue(all_ok)
        self.assertEqual(len(res), 3)

    def testExecuteBatchDelete(self):
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 0, 'shardKey': 1, 'name': 'A', 'age': 10}))
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 1, 'shardKey': 1, 'name': 'B', 'age': 20}))
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 2, 'shardKey': 1, 'name': 'C', 'age': 30}))
        batch = [Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_DELETE}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 0, 'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_DELETE}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 1, 'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_DELETE}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 2, 'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 })]
        res = self.store.execute_updates(batch)
        self.assertEqual(len(res), 3)
        all_ok = True
        for r in res:
            if (r[ONDB_WAS_SUCCESSFUL] is False):
                all_ok = False
                break
        self.store.multi_delete(self.table + "TableTest",
            Row({'shardkey': 1}))
        self.assertTrue(all_ok)

    def testExecuteBatchDeleteIfVersion(self):
        versions = []
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 0, 'shardKey': 1, 'name': 'A', 'age': 10}))
        versions.append(v)
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 1, 'shardKey': 1, 'name': 'B', 'age': 20}))
        versions.append(v)
        v, r = self.store.put(
            self.table + "TableTest",
            Row({'id': 2, 'shardKey': 1, 'name': 'C', 'age': 30}))
        versions.append(v)
        batch = [Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_DELETE_IF_VERSION}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 0, 'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True,
                  ONDB_VERSION: versions[0]
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_DELETE_IF_VERSION}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 1, 'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True,
                  ONDB_VERSION: versions[1]
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_DELETE_IF_VERSION}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 2, 'shardkey': 1}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True,
                  ONDB_VERSION: versions[2]
                 })]
        res = self.store.execute_updates(batch)
        self.assertEqual(len(res), 3)
        all_ok = True
        for r in res:
            if (r[ONDB_WAS_SUCCESSFUL] is False):
                all_ok = False
                break
        self.store.multi_delete(self.table + "TableTest",
            Row({'shardkey': 1}))
        self.assertTrue(all_ok)

    def testExecuteBatchWrongTableKeyName(self):
        batch = [{ONDB_OPERATION: ONDB_PUT,
                  'TableName': self.table,
                  ONDB_ROW: Row({'id': 1, 'name': 'John', 'age': 25,
                      'shardkey': 0}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }]
        self.assertRaises(KeyError, self.store.execute_updates,
            batch)

    def testExecuteBatchWrongOpertionType(self):
        batch = [{ONDB_OPERATION: 'GET',
                  ONDB_TABLE_NAME: self.table,
                  ONDB_ROW: Row({'id': 1, 'name': 'John', 'age': 25,
                      'shardkey': 0}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }]
        self.assertRaises(IllegalArgumentException, self.store.execute_updates,
            batch)

    def testExecuteBatchOperationsOnRowsWithTTL(self):
        hour_in_milliseconds = 60 * 60 * 1000
        ttl = TimeToLive({ONDB_TTL_VALUE: 3,
                          ONDB_TTL_TIMEUNIT: {ONDB_TIMEUNIT: ONDB_HOURS}})
        expect_expiration = ttl.calculate_expiration(time() * 1000)
        # Prepare a row for put_if_present operation. 
        self.store.put(self.table + "TableTest",
            Row({'id': 0, 'name': 'A', 'age': 10, 'shardkey': 0}))
        # Prepare a row for delete operation
        delete_row = Row({'id': 2, 'name': 'Rick', 'age': 31, 'shardkey': 0})
        delete_row.set_timetolive(ttl)
        self.store.put(self.table + "TableTest", delete_row)
        # row0 is used for updating the row with id=0
        row0 = Row({'id': 0, 'name': 'John', 'age': 25, 'shardkey': 0})
        row0.set_timetolive(ttl)
        # row1 is used for put_if_absent operation
        row1 = Row({'id': 1, 'name': 'Chris', 'age': 30, 'shardkey': 0})
        row1.set_timetolive(ttl)
        batch = [Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_PRESENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: row0,
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_PUT_IF_ABSENT}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: row1,
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 }), Operation({
                  ONDB_OPERATION: OperationType({
                     ONDB_OPERATION_TYPE: ONDB_DELETE}),
                  ONDB_TABLE_NAME: self.table + "TableTest",
                  ONDB_ROW: Row({'id': 2, 'shardkey': 0}),
                  ONDB_ABORT_IF_UNSUCCESSFUL: True
                 })]
        write_op = WriteOptions({ONDB_UPDATE_TTL: True})
        res = self.store.execute_updates(batch, write_op)
        self.assertEqual(len(res), 3)
        count = 0
        get_res = self.store.multi_get(self.table + "TableTest",
                                       Row({'shardkey': 0}), False)
        for r in get_res:
            actual_expiration = r.get_expiration()
            actual_expect_diff = actual_expiration - expect_expiration
            self.assertGreater(actual_expiration, 0)
            self.assertLess(actual_expect_diff, hour_in_milliseconds)
            self.assertGreaterEqual(actual_expect_diff, 0)
            count += 1
        self.assertEqual(count, 2)
        self.store.multi_delete(self.table + "TableTest", Row({'shardkey': 0}))


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
