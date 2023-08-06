import boto3
import logging
import os

from sys import exit as sys_exit
from click import echo
from botocore.exceptions import ClientError

logging.getLogger('botocore').setLevel(logging.NOTSET)
logging.getLogger('boto3').setLevel(logging.NOTSET)

client = boto3.client('sts')


def assume_role(role_arn, session_name, external_id=None, mfa_device_serial_number=None, mfa_token=None):
    '''Assumes role with/without external_id and mfa_token
    '''

    sts_kwargs = {'RoleArn': role_arn, 'RoleSessionName': session_name}

    if external_id is None:
        try:
            # try to load from environment
            external_id = os.environ['AWS_STS_EXTERNAL_ID']
        except KeyError:
            pass

    if external_id:
        sts_kwargs.update({'ExternalId': str(external_id)})

    if mfa_token and mfa_device_serial_number:
        sts_kwargs.update({'TokenCode': str(mfa_token),
                           'SerialNumber': str(mfa_device_serial_number)})

    try:
        response = client.assume_role(**sts_kwargs)
    except ClientError as e:
        echo(e, err=True)
        if ('AccessDenied' in str(e)) and (not mfa_token) and (not 'MFA' in str(e)):
            echo('# Please check your Role trust policy and your IAM Policy, or, you might need to supply MFA.', err=True)
        sys_exit(1)
    except Exception:
        raise

    return response


def assume_role_with_saml():
    pass


def assume_role_with_web_identity():
    pass
