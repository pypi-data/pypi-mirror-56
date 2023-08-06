from unittest import TestCase

from aws.cfm import *

class TestCloudFormation(TestCase):

    def test_get_stack_status_fail(self):
        status = get_stack_status('bogus')
        self.assertEqual('Status not found', status)

    def test_get_stack_fail(self):
        stack = get_stack('bogus')
        self.assertIsNone(stack)

    def test_stack_exists_none(self):
        self.assertFalse(stack_exists('bogus'))

