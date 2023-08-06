from unittest import TestCase, mock

from aws.ec2 import *
from aws.region import *
from aws.cfm import *

from po.pretty_object import PrettyObject
import pprint

po = PrettyObject()
pp = pprint.PrettyPrinter(indent=2, width=40)


def abs_path(file: str):
    """
    Sets an absolute path relative to the **k9** package directory.

    Example::
        result = abs_path('myfile)

    Result::
        /Users/simon/git/k9/k9/myfile


    This is used primarily for building unit tests within the K9 package
    and is not expected to be useful to K9 library users.

    :param file: File or directory to attach absolute path with
    :return: absolute path to specified file or directory
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(basedir, file)


class TestEc2(TestCase):

    def test_get_regions(self):
        region = 'us-east-2'
        set_default_region(region)
        regions = list_regions()
        found = [
            region['RegionName']
            for region in regions
            if region['RegionName'] == 'us-east-2'
        ]
        self.assertEqual(1, len(found))

    def test_list_azs(self):
        azs = list_azs()
        found = [
            az['ZoneName']
            for az in azs
            if az['ZoneName'] == 'us-east-2a'
        ]
        self.assertEqual(1, len(found))

    def test_default_region(self):
        region = 'us-east-2'
        set_default_region(region)
        self.assertEqual(region, get_default_region())

    def test_all(self):
        try:
            # Create the stack to test against
            stack1_name = 'unit-00-rancher-vpc'
            stack2_name = 'unit-01-rancher-bastion'
            key_name = 'unit-key_pair'
            kp = create_key_pair(key_name)

            parameters = {
                'EnvType': 'unit',
                'CidrPrefix': '10.222',
                'DomainName': 'unit.simoncomputing.com',
                'KeyName': key_name
            }

            # Test create_stack
            stack = create_stack(abs_path('00-rancher-vpc.yaml'), parameters)
            self.assertTrue(stack_exists(stack1_name))

            # Test second try without failure
            stack = create_stack(abs_path('00-rancher-vpc.yaml'), parameters)

            stack = create_stack(abs_path('01-rancher-bastion.yaml'), {'EnvType': 'unit'})
            self.assertTrue(stack_exists(stack2_name))

            # Test get_stack()
            stack = get_stack(stack1_name)
            self.assertIsNotNone(stack)

            self.try_default_vpc()
            self.try_list_vpcs()
            self.try_list_subnets()
            self.try_security_groups()
            self.try_list_igws()
            self.try_list_nats()
            self.try_list_eips()
            self.try_list_route_tables()
            self.try_get_route_table()
            self.try_list_get_instances()


        finally:
            # If you are testing something repeatedly, you could comment the
            # delete statements out so that you don't have to re-create the
            # stacks to perform your testing.  The create actions will not
            # execute if the keypairs and stacks already exist.

            delete_key_pair(key_name)
            delete_stack(stack2_name)
            delete_stack(stack1_name)
            pass

    ###########################################################################
    # VPC
    ###########################################################################

    def try_default_vpc(self):

        vpc = get_vpc(name='unit-rancher-vpc')
        self.assertIsNotNone(vpc)

        vpcid = get_vpcid(vpc)
        self.assertIsNotNone(vpcid)

        set_current_vpcid(vpc)
        self.assertEqual(vpcid, get_current_vpcid())

        set_current_vpcid()
        set_current_vpcid(vpc)
        self.assertEqual(vpcid, get_current_vpcid())

        set_current_vpcid()
        set_current_vpcid(vpcid=vpcid)
        self.assertEqual(vpcid, get_current_vpcid())

    def try_list_vpcs(self):
        # List just the default
        vpc = get_vpc(default=True)
        self.assertIsNotNone(vpc)
        self.assertTrue(vpc['IsDefault'])

        # List by name
        vpc = get_vpc(name="default-vpc")
        self.assertIsNotNone(vpc)
        self.assertTrue(vpc['IsDefault'])
        vpcids = [vpc.get('VpcId')]

        vpc = get_vpc(name="unit-rancher-vpc")
        self.assertIsNotNone(vpc)
        vpcids.append(vpc.get('VpcId'))

        vpc = get_vpc(vpcid=get_vpcid(vpc))
        self.assertIsNotNone(vpc)
        self.assertTrue('unit-rancher-vpc', get_tag_value(vpc, 'Name'))

        # List all
        vpcs = list_vpcs()
        self.assertTrue(len(vpcs) > 0)
        found = [
            vpc
            for vpc in vpcs
            if vpc.get('VpcId') in vpcids
        ]
        self.assertEqual(2, len(found))

    def test_vpc_failures(self):
        result = get_vpc(vpcid='bogus')
        self.assertIsNone(result)

        set_current_vpcid(None)
        with self.assertRaisesRegex(Exception, 'You must call set_current_vpc()'):
            get_current_vpcid()

        with self.assertRaisesRegex(Exception, 'You must call set_current_vpc()'):
            get_vpc_filter()

        with self.assertRaisesRegex(Exception, 'default, name or vpcid must be provided when calling get_vpc()'):
            get_vpc()

    ###########################################################################
    # Subnets
    ###########################################################################

    def try_list_subnets(self):
        set_current_vpcid(get_vpc(name="unit-rancher-vpc"))
        vpcid = get_current_vpcid()

        for subnet in list_subnets():
            self.assertEqual(vpcid, get_vpcid(subnet))

        # Call with subnet_type
        subnets = list_subnets(subnet_type='private')
        for subnet in subnets:
            self.assertEqual('private', get_tag_value(subnet, 'SubnetType'))

        # Call with filter
        subnets = list_subnets({'SubnetType': 'public'})
        for subnet in subnets:
            self.assertEqual('public', get_tag_value(subnet, 'SubnetType'))

        subnet_id = get_subnet_id(subnets[0])
        subnet = get_subnet(subnet_id)
        self.assertEqual(subnet_id, get_subnet_id(subnet))

    def test_get_subnet(self):
        set_current_vpcid(get_vpc(default=True))

        subnet = get_subnet("bogus")
        self.assertIsNone(subnet)

    ###########################################################################
    # Internet Gateways & NATs
    ###########################################################################
    def try_list_igws(self):
        igws = list_igws()
        self.assertIsNotNone(igws)

        igw = get_vpc_igw()
        self.assertIsNotNone(igw)
        self.assertEqual(get_current_vpcid(), igw['Attachments'][0]['VpcId'])

    def try_list_nats(self):
        nats = list_nats()
        self.assertIsNotNone(nats)

        current_vpcid = get_current_vpcid()
        for nat in nats:
            self.assertEqual(current_vpcid, nat.get('VpcId'))

    def try_list_eips(self):
        eips = list_eips()
        self.assertIsNotNone(eips)

    ###########################################################################
    # Route Tables
    ###########################################################################

    def try_list_route_tables(self):
        current_vpcid = get_current_vpcid()

        rts = list_route_tables()
        for rt in rts:
            self.assertEqual(current_vpcid, rt.get('VpcId'))

        name = 'unit-public-rt'
        criteria = {'Name': name}
        rts = list_route_tables(criteria)
        for rt in rts:
            self.assertTrue(name, get_tag_value(rt, 'Name'))

    def try_get_route_table(self):
        name = 'unit-public-rt'
        rt = get_route_table(name)
        self.assertIsNotNone(name)
        self.assertEqual(name, get_tag_value(rt, 'Name'))

        rt_id = get_route_table_id(rt)

        rt = get_route_table(rt_id= rt_id)
        self.assertIsNotNone(name)
        self.assertEqual(name, get_tag_value(rt, 'Name'))

        subnets = list_subnets(subnet_type='public')
        subnet_id = get_subnet_id(subnets[0])

        rt = get_route_table(subnet_id= subnet_id)
        self.assertIsNotNone(rt)
        self.assertEqual(name, get_tag_value(rt, 'Name'))

        subnets = list_subnets(subnet_type='private')
        subnet_id = get_subnet_id(subnets[0])

        rt = get_route_table(subnet_id= subnet_id)
        self.assertIsNotNone(45)
        self.assertEqual('unit-private-rt', get_tag_value(rt, 'Name'))


    def test_get_route_table(self):
        set_current_vpcid(get_vpc(default=True))

        rt = get_route_table(name='bogus')
        self.assertIsNone(rt)

        rt = get_route_table(rt_id='bogus')
        self.assertIsNone(rt)

        rt = get_route_table(subnet_id='bogus')
        self.assertIsNone(rt)

        with self.assertRaisesRegex(Exception, 'name, rt_id or subnet_id must be specified'):
            get_route_table()

    ###########################################################################
    # Security Groups
    ###########################################################################

    def try_security_groups(self):
        sgs = list_sgs({'Name': 'unit-https-all-sg'})
        self.assertEqual(1, len(sgs))
        self.assertEqual('unit-https-all-sg', get_tag_value(sgs[0], 'Name'))

        sgs = list_sgs({'Name': 'unit-https-all-sg'})

        sg = get_sg(name='unit-https-all-sg')
        self.assertIsNotNone(sg)
        self.assertEqual('unit-https-all-sg', get_tag_value(sg, 'Name'))
        sgid = get_sgid(sg)

        sg = get_sg(sgid=sgid)
        self.assertIsNotNone(sg)
        self.assertEqual('unit-https-all-sg', get_tag_value(sg, 'Name'))

    def test_get_security_group_fail(self):
        set_current_vpcid(get_vpc(default=True))

        sg = get_sg(name="bogus")
        self.assertIsNone(sg)

        sgid = get_sgid({})
        self.assertIsNone(sgid)

        with self.assertRaisesRegex(Exception, 'You must provide name or sgid'):
            get_sg()


    ###########################################################################
    # Tags
    ###########################################################################
    def test_get_tags(self):
        vpc = {
            'CidrBlock': '172.31.0.0/16',
            'CidrBlockAssociationSet': [
                {
                    'AssociationId': 'vpc-cidr-assoc-d27fffbe',
                    'CidrBlock': '172.31.0.0/16',
                    'CidrBlockState': {
                        'State': 'associated'
                    }
                }
            ],
            'DhcpOptionsId': 'dopt-905f0feb',
            'InstanceTenancy': 'default',
            'IsDefault': True,
            'OwnerId': '862586795542',
            'State': 'available',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'default-vpc'
                }
            ],
            'VpcId': 'vpc-b43582ce'
        }

        tags = get_tags(vpc)
        self.assertEqual('default-vpc', tags['Name'])

    def test_get_tag_fail(self):
        result = get_tag_value({'Tags':[{'Key': 'Name','Value': 'default-vpc'}]}, 'Namex')
        self.assertIsNone(result)

    def test_match_tags(self):
        vpc = {
            'InstanceTenancy': 'default',
            'IsDefault': True,
            'State': 'available',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'default-vpc'
                },
                {
                    'Key': 'EnvType',
                    'Value': 'dev'
                }
            ],
            'VpcId': 'vpc-b43582ce'
        }

        self.assertTrue(match_tags({'Name':'default-vpc'}, vpc))
        self.assertFalse(match_tags({'Name':'bogus'}, vpc))
        self.assertTrue(match_tags({'Name':'default-vpc', 'EnvType': 'dev'}, vpc))
        self.assertFalse(match_tags({'Name':'default-vpc', 'EnvType': 'test'}, vpc))
        self.assertFalse(match_tags({'Name':'bogus'}, {}))

    ###########################################################################
    # KeyPairs
    ###########################################################################

    def test_key_pairs(self):
        try:
            # Test create_key_pair()
            name = "unit-kp"
            kp = create_key_pair(name)
            self.assertEqual(name, kp.get('KeyName'))

            # Test key_pair_exists()
            self.assertTrue(key_pair_exists(name))

            # Test list_key_pairs()
            kps = list_key_pairs()
            found = [
                kp
                for kp in kps
                if kp.get('KeyName') == name
            ]
            self.assertEqual(1, len(found))
            self.assertEqual(name, found[0].get('KeyName'))

            # Test delete_key_pair()
            delete_key_pair(name)
            self.assertFalse(key_pair_exists(name))

        finally:
            delete_key_pair(name)

    ###########################################################################
    # AMIs
    ###########################################################################
    def test_get_linux2_ami(self):
        imageid = get_linux2_ami()
        self.assertIsNotNone(imageid)

        response = get_image(imageid)
        self.assertIsNotNone(response)

    ###########################################################################
    # EC2 Instances
    ###########################################################################

    def try_list_get_instances(self):

        # Test list_instance()
        instances = list_instances()
        self.assertTrue(len(instances) > 0)

        # Test list_instance(search_filter)
        name = 'unit-bastion'
        instances = list_instances({'Name': name})
        self.assertEqual(1, len(instances))
        self.assertEqual(name, get_tag_value(instances[0], 'Name'))

        # Test get_instance(name)
        instance = get_instance(name)
        self.assertIsNotNone(instance)
        self.assertEqual(name, get_tag_value(instance, 'Name'))

        instance = get_instance(name=name)
        self.assertIsNotNone(instance)
        self.assertEqual(name, get_tag_value(instance, 'Name'))

        # Test get_instance(instance_id)
        instance_id = get_instance_id(instances[0])
        instance = get_instance(instance_id=instance_id)
        self.assertIsNotNone(instance)
        self.assertEqual(name, get_tag_value(instance, 'Name'))


    def test_get_instance_fail(self):
        set_current_vpcid(get_vpc(default=True))

        instance = get_instance('bogus')
        self.assertIsNone(instance)

        instance = get_instance(name='bogus')
        self.assertIsNone(instance)

        instance = get_instance(instance_id='bogus')
        self.assertIsNone(instance)

        with self.assertRaisesRegex(Exception, 'name or instance_id must be provided'):
            get_instance()

