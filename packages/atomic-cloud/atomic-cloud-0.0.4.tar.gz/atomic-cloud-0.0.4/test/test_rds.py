import unittest
from unittest import TestCase, mock
from aws.rds import *


class TestRds(TestCase):

###########################################################################
# Database Clusters & Instances
###########################################################################

    def test_list_db_clusters(self):
        clusters = list_db_clusters()
        found = [
            cluster['DBClusterIdentifier']
            for cluster in clusters
            if cluster['DBClusterIdentifier'] == 'database-1'
        ]
        self.assertEqual(1, len(found))

    def test_get_db_cluster(self):
        cluster = get_db_cluster('database-1')
        self.assertIsNotNone(cluster)

    def test_get_db_cluster_fail(self):
        cluster = get_db_cluster('invalid-cluster')
        self.assertEqual(0, len(cluster))

    @unittest.expectedFailure
    def test_set_deletion_protection_cluster(self):
        set_db_cluster_delete_protection('database-1', True)
        delete_cluster('database-1')

    def test_list_db_instances(self):
        instances = list_db_instances()
        found = [
            instance['DBInstanceIdentifier']
            for instance in instances
            if instance['DBInstanceIdentifier'] == 'database-1-instance-1'
        ]
        self.assertEqual(1, len(found))


    def test_get_db_instance(self):
        instance = get_db_instance('database-1-instance-1')
        self.assertIsNotNone(instance)

    def test_get_db_instance_fail(self):
        instance = get_db_instance('invalid-instance')
        self.assertEqual(0, len(instance))

    @unittest.expectedFailure
    def test_set_deletion_protection_instance(self):
        set_db_instance_delete_protection('database-1-instance-1', True)
        delete_instance('database-1-instance-1')

###########################################################################
# Database Subnet Groups
###########################################################################

    def test_list_subnet_groups(self):
        groups = list_subnet_groups()
        found = [
            group['DBSubnetGroupName']
            for group in groups
            if group['DBSubnetGroupName'] == 'default'
        ]
        self.assertEqual(1, len(found))

    def test_get_subnet_group(self):
        group = get_subnet_group('default')
        self.assertIsNotNone(group)

    @unittest.expectedFailure
    def test_get_subnet_group_fail(self):
        group = get_subnet_group('invalid-subnet-group')
        self.assertIsNone(group)

###########################################################################
# Database Security Groups
###########################################################################

    def test_list_db_sgs(self):
        sec_groups = list_db_sgs()
        found = [
            sec_group['DBSecurityGroupName']
            for sec_group in sec_groups
            if sec_group['DBSecurityGroupName'] == 'default'
        ]

    def test_get_db_sg(self):
        sec_group = get_db_sg('default')
        self.assertIsNotNone(sec_group)


    