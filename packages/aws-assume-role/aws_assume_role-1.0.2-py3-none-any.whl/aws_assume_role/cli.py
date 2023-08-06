import click
import sys
import os
import boto3
import time
import re

from botocore.exceptions import ClientError
from aws_assume_role import __version__
from aws_assume_role import utils


def version_message():
    """Return the version"""
    python_version = sys.version[:3]
    message = u'aws-assume-role version %(version)s (Python {})'
    return message.format(python_version)


@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.version_option(__version__, u'-V', u'-v', u'--version', message=version_message())
@click.option(
    '--account-id', '--account', type=str, required=False,
    help=u'The explicit account id to assume the role from. '
         u'Defaults to the current user account id'
)
@click.option(
    u'--role-name', type=str, required=True,
    help=u'The role name to assume'
)
@click.option(
    u'--external-id', type=str, required=False,
    help='External id to supply'
)
@click.option(
    u'--mfa-token', type=str, required=False,
    help='The MFA token to pass if using MFA'
)
def main(account_id, role_name, external_id, mfa_token):
    """Assumes AWS Role based on the provided explicit account_id and role_name
    Or based on the configured local aws configuration file.
    """

    import logging
    logging.getLogger('botocore').setLevel(logging.NOTSET)
    logging.getLogger('boto3').setLevel(logging.NOTSET)

    client = boto3.client('sts')

    try:
        caller = client.get_caller_identity()
    except ClientError as e:
        click.echo(e)
        sys.exit(1)
    except Exception:
        raise

    caller_id = caller['UserId']
    caller_account_id = caller['Account']
    millis = int(round(time.time() * 1000))

    session_name = 'aws_assume_{}_{}'.format(caller_id, millis)

    if account_id is None:
        account_id = caller_account_id
    elif not re.match(r'^\d{12}\b$', account_id):
        account_id_dict = utils.load_account_ids_from_account_file()
        try:
            account_id = account_id_dict[account_id]
        except KeyError as e:
            click.echo('Account alias {} not found.'.format(e))
            click.echo(
                'Please check your inputted alias or .aws/accounts file!')
            sys.exit(1)

    if external_id is None:
        try:
            external_id = os.environ['AWS_STS_EXTERNAL_ID']
        except KeyError:
            pass

    role_arn = 'arn:aws:iam::{}:role/{}'.format(account_id, role_name)

    try:
        if external_id:
            response = client.assume_role(
                RoleArn=role_arn, RoleSessionName=session_name, ExternalId=external_id)
        else:
            response = client.assume_role(
                RoleArn=role_arn, RoleSessionName=session_name)
    except ClientError as e:
        click.echo(e)
        sys.exit(1)
    except Exception:
        raise

    assumed_access_key_id = response['Credentials']['AccessKeyId']
    assumed_secret_access_key = response['Credentials']['SecretAccessKey']
    assumed_session_token = response['Credentials']['SessionToken']

    click.echo('export AWS_ACCESS_KEY_ID={}'.format(assumed_access_key_id))
    click.echo('export AWS_SECRET_ACCESS_KEY={}'.format(
        assumed_secret_access_key))
    click.echo('export AWS_SESSION_TOKEN={}'.format(assumed_session_token))
    click.echo('export ASSUMED_ROLE={}'.format(role_arn))
