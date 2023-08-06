import os
import sys
import time
import itertools

import boto3

from po.pretty_object import PrettyObject

###############################################################################
# CloudFormation
###############################################################################

# Stack Status Values
CREATE_COMPLETE = 'CREATE_COMPLETE'
CREATE_IN_PROGRESS = 'CREATE_IN_PROGRESS'
CREATE_FAILED = 'CREATE_FAILED'
ROLLBACK_IN_PROGRESS = 'ROLLBACK_IN_PROGRESS'
ROLLBACK_FAILED = 'ROLLBACK_FAILED'
ROLLBACK_COMPLETE = 'ROLLBACK_COMPLETE'
DELETE_IN_PROGRESS = 'DELETE_IN_PROGRESS'
DELETE_FAILED = 'DELETE_FAILED'
DELETE_COMPLETE = 'DELETE_COMPLETE'
UPDATE_IN_PROGRESS = 'UPDATE_IN_PROGRESS'
UPDATE_COMPLETE_CLEANUP_IN_PROGRESS = 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS'
UPDATE_COMPLETE = 'UPDATE_COMPLETE'
UPDATE_ROLLBACK_IN_PROGRESS = 'UPDATE_ROLLBACK_IN_PROGRESS'
UPDATE_ROLLBACK_FAILED = 'UPDATE_ROLLBACK_FAILED'
UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS = 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS'
UPDATE_ROLLBACK_COMPLETE = 'UPDATE_ROLLBACK_COMPLETE'
REVIEW_IN_PROGRESS = 'REVIEW_IN_PROGRESS'

# Capability Values
CAPABILITY_IAM = 'CAPABILITY_IAM'
CAPABILITY_NAMED_IAM = 'CAPABILITY_NAMED_IAM'
CAPABILITY_AUTO_EXPAND = 'CAPABILITY_AUTO_EXPAND'

cfn = boto3.client('cloudformation')
po = PrettyObject()


def get_stack_status(stack_name: str):
    """
    Extracts just the StackStatus field.  This is useful for
    waiting on the stack for a status change.

    :param stack_name: Stack to query.
    :return: string value of status
    """
    stacks = cfn.list_stacks()['StackSummaries']
    for stack in stacks: 
        if stack.get('StackName') == stack_name:
            return stack['StackStatus']
    return 'Status not found'


def get_stack(stack_name: str):
    """
    Gets the stack information.

    :param stack_name: Stack to query.
    :return: `cloudformation.Stack <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#stack>`_
    """
    stacks = cfn.describe_stacks()['Stacks']
    for stack in stacks: 
        if stack.get('StackName') == stack_name:
            return stack
    return None


def stack_exists(stack_name: str):
    """
    Returns true if StackStatus == CREATE_COMPLETE
    :param stack_name: Name of stack
    :return: True if StackStatus is CREATE_COMPLETE
    """
    stacks = cfn.list_stacks()['StackSummaries']

    for stack in stacks: 
        if stack['StackStatus'] == CREATE_COMPLETE:
            if stack.get('StackName') == stack_name:
                return True

    return False


def wait_for_stack(stack_name: str, pend_status: str):
    """
    Waits for the specified pend_status to clear.   This function
    will provide a spinner while waiting for the status to change.

    :param stack_name: Name of stack to observe.
    :param pend_status: Status we will wait on until it changes.  For
    example, if the pend_status == CREATE_IN_PROGRESS, we'll wait until
    it changes to something else like CREATE_COMPLETED.

    :return:
    """
    spinner = itertools.cycle('-\\|/')

    status = pend_status
    print(status)
    while status == pend_status:
        sys.stdout.write(spinner.__next__())  # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')   
        time.sleep(1)
        status = get_stack_status(stack_name)

    print(status)
    return status


def create_stack(fn: str, params={}, capabilities=[], stack_name: str = None):
    """
    Creates a cloud formation stack

    :param fn: File name of cloud formation template
    :param params: Parameters required by the template
    :param capabilities: Used to add IAM capabilities if we are doing
    something that is powerful such as creating roles.
    :param stack_name: Used to specify a non-standard stack name
    :return: `cloudformation.Stack <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#stack>`_
    """
    file = None

    try:
        # create stack name
        (_, filename) = os.path.split(fn)
        if stack_name is None:
          stack_name = params['EnvType'] + '-' + filename.split('.')[0]

        # if stack already exists, skip and return true
        if stack_exists(stack_name):
            print(f"{stack_name} already exists - skipping stack creation.")
            return True

        print(f"Creating {stack_name}...")

        # read template
        file = open(fn)
        template = file.read()

        # get params list
        template_validated = cfn.validate_template(TemplateBody=template)

        # create parameters
        cfn_params = [
            {'ParameterKey': kvp['ParameterKey'], 'ParameterValue': params[kvp['ParameterKey']]}
            for kvp in template_validated['Parameters']
        ]

        # create stack
        metadata = cfn.create_stack(StackName=stack_name,
                                   TemplateBody=template,
                                   Parameters=cfn_params,
                                   Capabilities=capabilities,
                                   OnFailure="DO_NOTHING")

        # wait for the stack
        status = wait_for_stack(stack_name, CREATE_IN_PROGRESS)
        summary = get_stack(stack_name)
        po.print(summary)

        if status != CREATE_COMPLETE: 
            raise Exception(f'Stack creation failed: {stack_name}')

        return summary

    except IOError as e:
        print(f"Can't open stack {e}") 

    finally: 
        if file is not None:
            file.close()

def get_export_value(stack_name: str, export_name: str):
    """
    Gets a value that the given stack has exported

    :param stack_name: the name of the stack that exports the value
    :param export_name: the exported name (unique)
    :return: the exported value as a string
    """
    outs = get_stack(stack_name)['Outputs']
    if not outs:
      return None
    for out in outs:
      if out['ExportName'] == export_name:
        return out['OutputValue']

def delete_stack(stack_name: str):
    """
    Deletes the specified stack.

    :param stack_name: Name of stack to remove
    :return: Last known status.
    """
    print(f'Deleting {stack_name}...')
    cfn.delete_stack(StackName=stack_name)
    status = wait_for_stack(stack_name, DELETE_IN_PROGRESS)

    return status
