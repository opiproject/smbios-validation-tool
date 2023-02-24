"""Tests for google3.third_party.py.smbios_validation_tool.error_bucket."""

from smbios_validation_tool.error_bucket import ErrorBucket
import unittest


class ErrorBucketTest(unittest.TestCase):

  def setUp(self):
    super(ErrorBucketTest, self).setUp()
    self.error_bucket = ErrorBucket()

  def test_adding_errors_in_bucket(self):
    self.assertEqual(self.error_bucket.bucket,{})

    self.error_bucket.add_error('1', ('err_1', 'action_1'))
    self.error_bucket.add_error('1', ('err_2', 'action_2'))
    self.error_bucket.add_error('2', ('err_3', 'action_3'))

    current_bucket = self.error_bucket.bucket
    self.assertEqual(len(current_bucket), 2)
    self.assertEqual(current_bucket['1'], [('err_1', 'action_1'),
                                           ('err_2', 'action_2')])
    self.assertEqual(current_bucket['2'], [('err_3', 'action_3')])


if __name__ == '__main__':
  unittest.main()
