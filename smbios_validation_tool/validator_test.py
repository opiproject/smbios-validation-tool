# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for smbios_validation_tool.validator."""

import os

import dmiparse
from smbios_validation_tool import validator
import unittest

TEST_PATH = 'smbios_validation_tool/test_data'

tested_validators = [validator.RecordsPresenceChecker, 
                     validator.MemoryGroupAssociationsChecker]

class ValidatorTest(unittest.TestCase):

  def setUp(self):
    super(ValidatorTest, self).setUp()

    good_data_path = os.path.join(TEST_PATH, 'less_compliant_smbios_records.txt')
    self.good_records, self.good_groups = dmiparse.DmiParser(good_data_path).parse()

    bad_data_path = os.path.join(TEST_PATH, 'not_less_compliant_smbios_records.txt')
    self.bad_records, self.bad_groups = dmiparse.DmiParser(bad_data_path).parse()

  def testGoodDataPassesAllCheckersForGroupRecords(self):
    for checker in tested_validators:
        with self.subTest(checker):
          self.assertEqual(checker(self.good_records, self.good_groups).validate(),{})

  def testBadDataPromptsExpectedErrorMessagesForRecordsPresenceChecker(self):
    checker = validator.RecordsPresenceChecker(self.bad_records,
                                               self.bad_groups)

    expected_err_msgs = {'Motherboard SMBIOS record is missing.'}
    self.assertEqual(checker.validate().keys(), expected_err_msgs)

  def testBadDataPromptsExpectedErrorMessagesForMemoryGroupAssociationsChecker(
      self):
    checker = validator.MemoryGroupAssociationsChecker(self.bad_records,
                                                       self.bad_groups)
    err_msgs = checker.validate().keys()

    expected_err_msgs = {
        'Memory Controller Handle 0x0297 (IMC0) is not listed in any die record.',
        'Memory Controller Handle 0x0299 (IMC0) is not listed in any die record.',
        'Memory Controller Handle 0x0298 (IMC1) is not listed in any die record.',
        'There is no memory controller handle in items of Die Handle 0x02C9 '
        '(die0).',
        'Some items in Handle 0x0298 (IMC1) are not Type 14 handles (Group '
        'Associations).',
        'In items of Die Handle 0x02CC (die0), memory controller handle 0x029B'
        ' was belong to another die record (0x02CB).'
    }
    self.assertCountEqual(err_msgs, expected_err_msgs)


if __name__ == '__main__':
  unittest.main()
