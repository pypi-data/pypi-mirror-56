import click
import sys
import os
import boto3
import time
import re

from botocore.client import ClientError
from aws_assume_role import __version__
from aws_assume_role import utils
from aws_assume_role.assumer import client, assume_role, assume_role_with_saml, assume_role_with_web_identity
from aws_assume_role.options import Inclusive


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
    u'--mfa-device-serial-number', cls=Inclusive, required_with=["mfa_token"], type=str,
    help=u'The Serial Number of your MFA device. '
         u'Defaults to arn:aws:iam::ACCOUNT:mfa/CALLER_USER.'
)
@click.option(
    u'--mfa-token', type=str, required=False,
    help=u'The MFA token to pass if using MFA.'
)
def main(account_id, role_name, external_id, mfa_device_serial_number, mfa_token):
    """Assumes AWS Role based on the provided explicit account_id and role_name
    Or based on the configured local aws configuration file.
    """

    try:
        caller = client.get_caller_identity()
    except ClientError as e:
        click.echo(e)
        sys.exit(1)
    except Exception:
        raise

    caller_id = caller['UserId']
    caller_account_id = caller['Account']
    caller_arn = caller['Arn']
    millis = int(round(time.time() * 1000))

    session_name = 'aws_assume_{}_{}'.format(caller_id, millis)

    # defaults caller's account id
    if account_id is None:
        account_id = caller_account_id
        click.echo(
            '# You did not supply --account-id, using current caller id {} as target account_id. . .'.format(caller_account_id))
    # if account is supplied as alias, try finding the alias
    elif not re.match(r'^\d{12}\b$', account_id):
        account_id_dict = utils.load_account_ids_from_account_file()
        try:
            account_alias = account_id
            account_id = account_id_dict[account_alias]
            click.echo('# You supplied the alias \'{}\'. Using your configured {} as target account_id. . .'.format(
                account_alias, account_id))
        except KeyError as e:
            click.echo('Account alias {} not found.'.format(e))
            click.echo(
                'Please check your inputted alias or .aws/accounts file!')
            sys.exit(1)

    # defaults mfa_device_serial_number if mfa_token is supplied
    if (mfa_token) and (mfa_device_serial_number is None):
        mfa_device_serial_number = re.sub(r':user\/', ':mfa/', caller_arn)
        click.echo('# You supplied mfa_token without mfa_device_serial_number, using {} by default. . .'.format(
            mfa_device_serial_number))

    role_arn = 'arn:aws:iam::{}:role/{}'.format(account_id, role_name)

    response = assume_role(role_arn, session_name,
                           external_id, mfa_device_serial_number, mfa_token)

    try:
        assumed_access_key_id = response['Credentials']['AccessKeyId']
        assumed_secret_access_key = response['Credentials']['SecretAccessKey']
        assumed_session_token = response['Credentials']['SessionToken']
    except KeyError as e:
        click.echo('Something\'s wrong:', err=True)
        raise

    click.echo('export AWS_ACCESS_KEY_ID="{}"'.format(assumed_access_key_id))
    click.echo('export AWS_SECRET_ACCESS_KEY="{}"'.format(
        assumed_secret_access_key))
    click.echo('export AWS_SESSION_TOKEN="{}"'.format(assumed_session_token))
    click.echo('export ASSUMED_ROLE="{}"'.format(role_arn))
