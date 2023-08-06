import boto3

###########################################################################
# Region
###########################################################################
_region = None

# AWS Clients
_ec2_client = None
_ecs_client = None
_elb_client = None
_elbv2_client = None
_iam_client = None
_rds_client = None


def set_default_region(region: str):
    """
    Initializes all library clients based on the specified region.  The library clients
    are AWS API clients that give us access to AWS.  Note that if you set the region with
    **aws configure**, that will take precedence.

    :param region: The region that all library clients will be opened with.
    :return: No return value.
    """
    global _region
    _region = region


def get_default_region():
    global _region

    if _region is None:
        raise Exception("You must call set_default_region() before calling get_default_region()")
    return _region


def get_ec2():
    global _ec2_client
    if _ec2_client is None:
        _ec2_client = boto3.client('ec2', _region)

    return _ec2_client


def get_ecs():
    global _ecs_client
    if _ecs_client is None:
        _ecs_client = boto3.client('ecs', _region)

    return _ecs_client


def get_elb():
    global _elb_client
    if _elb_client is None:
        _elb_client = boto3.client('elb', _region)

    return _elb_client


def get_elbv2():
    global _elbv2_client
    if _elbv2_client is None:
        _elbv2_client = boto3.client('elbv2', _region)

    return _elbv2_client


def get_iam():
    global _iam_client
    if _iam_client is None:
        _iam_client = boto3.client('iam', _region)

    return _iam_client


def get_rds():
    global _rds_client
    if _rds_client is None:
        _rds_client = boto3.client('rds', _region)

    return _rds_client
