from unittest import TestCase, mock

from aws.elb import *


from po.pretty_object import PrettyObject
import pprint


class TestElb(TestCase):

    ###########################################################################
    # Classic Load Balancer
    ###########################################################################

    def test_list_elbs(self):
        elbs = list_elbs()
        found = [
            elb['LoadBalancerName']
            for elb in elbs
            if elb['LoadBalancerName'] == 'unit-classic-loadbalancer'
        ]
        self.assertEqual(1, len(found))

    def test_get_elb_fail(self):
        elb = get_elb("null")
        self.assertIsNone(elb)

    def test_get_elb(self):
        elb = get_elb('unit-classic-loadbalancer')
        self.assertIsNotNone(elb)

    ###########################################################################
    # Application Load Balancer
    ###########################################################################

    def test_list_elbv2(self):
        elbv2s = list_elbv2s()
        found = [
            elbv2['LoadBalancerName']
            for elbv2 in elbv2s
            if elbv2['LoadBalancerName'] == 'unit-load-balancer'
        ]
        self.assertEqual(1, len(found))

    def test_get_elbv2(self):
        elbv2 = get_elbv2(name='unit-load-balancer')
        self.assertIsNotNone(elbv2)

    def test_get_elbv2_fail(self):
        elbv2 = get_elbv2('null')
        self.assertIsNone(elbv2)

    ###########################################################################
    # Target Groups
    ###########################################################################

    def test_list_target_groups(self):
        tgs = list_target_groups()
        found = [
            tg['TargetGroupName']
            for tg in tgs
            if tg['TargetGroupName'] == 'unit-worker-tg'
        ]
        self.assertEqual(1, len(found))

    def test_get_target_group(self):
        tg = get_target_group(name='unit-worker-tg')
        self.assertIsNotNone(tg)

    def test_get_target_group_fail(self):
        tg = get_target_group('null')
        self.assertIsNone(tg)

    def test_get_tag(self):
        pass

    def test_add_target(self):
      # add an instance
      # get target group info, look for it
      # Need consistent methodology for this testing. will do this once we've got that.
      # ran outside tests using specific configuration expectations that all passed.
      pass