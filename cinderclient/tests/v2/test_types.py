# Copyright (c) 2013 OpenStack Foundation
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cinderclient.v2 import volume_types
from cinderclient.tests import utils
from cinderclient.tests.v2 import fakes

cs = fakes.FakeClient()


class TypesTest(utils.TestCase):

    def test_list_types(self):
        tl = cs.volume_types.list()
        cs.assert_called('GET', '/types')
        for t in tl:
            self.assertIsInstance(t, volume_types.VolumeType)

    def test_list_types_not_public(self):
        cs.volume_types.list(is_public=None)
        cs.assert_called('GET', '/types?is_public=None')

    def test_create(self):
        t = cs.volume_types.create('test-type-3', 'test-type-3-desc')
        cs.assert_called('POST', '/types',
                         {'volume_type': {
                          'name': 'test-type-3',
                          'description': 'test-type-3-desc',
                          'os-volume-type-access:is_public': True
                          }})
        self.assertIsInstance(t, volume_types.VolumeType)

    def test_create_non_public(self):
        t = cs.volume_types.create('test-type-3', 'test-type-3-desc', False)
        cs.assert_called('POST', '/types',
                         {'volume_type': {
                          'name': 'test-type-3',
                          'description': 'test-type-3-desc',
                          'os-volume-type-access:is_public': False
                          }})
        self.assertIsInstance(t, volume_types.VolumeType)

    def test_update(self):
        t = cs.volume_types.update('1', 'test_desc_1')
        cs.assert_called('PUT', '/types/1')
        self.assertIsInstance(t, volume_types.VolumeType)

    def test_get(self):
        t = cs.volume_types.get('1')
        cs.assert_called('GET', '/types/1')
        self.assertIsInstance(t, volume_types.VolumeType)

    def test_default(self):
        t = cs.volume_types.default()
        cs.assert_called('GET', '/types/default')
        self.assertIsInstance(t, volume_types.VolumeType)

    def test_set_key(self):
        t = cs.volume_types.get(1)
        t.set_keys({'k': 'v'})
        cs.assert_called('POST',
                         '/types/1/extra_specs',
                         {'extra_specs': {'k': 'v'}})

    def test_unsset_keys(self):
        t = cs.volume_types.get(1)
        t.unset_keys(['k'])
        cs.assert_called('DELETE', '/types/1/extra_specs/k')

    def test_delete(self):
        cs.volume_types.delete(1)
        cs.assert_called('DELETE', '/types/1')
