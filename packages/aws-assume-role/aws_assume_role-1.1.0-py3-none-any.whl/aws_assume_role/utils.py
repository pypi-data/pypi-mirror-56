import json
import os
import click
import sys

from pathlib import Path


def load_account_ids_from_account_file(account_file=None) -> dict():
    home = str(Path.home())

    if account_file is None:
        account_file = '{}/.aws/accounts'.format(home)

    account_dict = dict()

    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            try:
                account_dict = json.load(f)
            except json.decoder.JSONDecodeError as e:
                click.echo('An error found at your account file.')
                click.echo(
                    'JSON might be malformed in {}'.format(account_file))
                click.echo(e)
                sys.exit(1)
            except Exception:
                raise

    return account_dict
