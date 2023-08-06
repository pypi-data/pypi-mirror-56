import logging

import click
from botocore.exceptions import ClientError
from click.exceptions import Exit

from .manager import Manager

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = logging.getLogger(__name__)


def gitlab_issue_url(subject, body):
    from urllib.parse import urlencode
    params = urlencode({
        'issue[title]': subject,
        'issue[description]': body,
    })
    url = "https://gitlab.com/perobertson/aws-credentials/issues/new?{params}".format(
        params=params
    )
    return url


def warn_unexpected_response(action, response):
    subject = "Unexpected response for {action}".format(
        action=action
    )
    body = "Response from AWS: `{response}`".format(
        response=response
    )
    url = gitlab_issue_url(subject, body)
    msg = 'WARNING: Unexpected response from AWS. '\
          'Please consider opening an issue with the response details.\n\n'\
          "{url}".format(url=url)
    print(msg)


def validate_aws_vars(ctx, param, value):
    if value == '':
        raise click.BadParameter('cannot be blank.')
    return value


def init_logging(level):
    try:
        from termcolor import colored
    except ImportError:
        def colored(text, *args, **kwargs):
            return text

    fmt = colored(
        '%(levelname)-8s %(asctime)s [%(name)s] %(filename)s:%(lineno)-3s',
        'cyan'
    ) + colored(
        ' %(funcName)s',
        'yellow'
    ) + ' %(message)s'

    root_logger = logging.getLogger(__name__.split('.')[0])
    root_logger.setLevel(level)
    formatter = logging.Formatter(fmt)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    root_logger.addHandler(sh)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose',
              count=True,
              help='Increase the verbosity of messages: "-v" for normal output, and "-vv" for more verbose output.')
def cli(verbose):
    """CLI utility for managing access keys."""
    if verbose == 1:
        init_logging(logging.INFO)
    elif verbose == 2:
        init_logging(logging.DEBUG)
    else:
        init_logging(logging.WARNING)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--access-key',
              help='AWS_ACCESS_KEY_ID to use.',
              envvar='AWS_ACCESS_KEY_ID',
              callback=validate_aws_vars)
@click.option('--secret-key',
              help=' AWS_SECRET_ACCESS_KEY to use.',
              envvar='AWS_SECRET_ACCESS_KEY',
              callback=validate_aws_vars)
@click.option('--session-token',
              help='AWS_SESSION_TOKEN to use.',
              envvar='AWS_SESSION_TOKEN',
              callback=validate_aws_vars)
def list(access_key, secret_key, session_token):
    """List access keys."""
    mgr = Manager(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token)
    keys = mgr.keys()
    headers = 'AccessKeyId', 'Status', 'CreateDate'
    print("{:20} {:8} {}".format(*headers))
    for key in keys:
        print("{} {:8} {}".format(key['AccessKeyId'], key['Status'], key['CreateDate']))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--access-key',
              help='AWS_ACCESS_KEY_ID to use.',
              envvar='AWS_ACCESS_KEY_ID',
              callback=validate_aws_vars)
@click.option('--secret-key',
              help=' AWS_SECRET_ACCESS_KEY to use.',
              envvar='AWS_SECRET_ACCESS_KEY',
              callback=validate_aws_vars)
@click.option('--session-token',
              help='AWS_SESSION_TOKEN to use.',
              envvar='AWS_SESSION_TOKEN',
              callback=validate_aws_vars)
def create(access_key, secret_key, session_token):
    """Create a new access key."""
    mgr = Manager(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token)
    try:
        response = mgr.create()
    except ClientError as e:
        print(e)
        raise Exit(1)
    key = response['AccessKey']
    msg = "UserName:        {}\n"\
          "AccessKeyId:     {}\n"\
          "SecretAccessKey: {}".format(key['UserName'], key['AccessKeyId'], key['SecretAccessKey'])
    print(msg)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--access-key',
              help='AWS_ACCESS_KEY_ID to use.',
              envvar='AWS_ACCESS_KEY_ID',
              callback=validate_aws_vars)
@click.option('--secret-key',
              help=' AWS_SECRET_ACCESS_KEY to use.',
              envvar='AWS_SECRET_ACCESS_KEY',
              callback=validate_aws_vars)
@click.option('--session-token',
              help='AWS_SESSION_TOKEN to use.',
              envvar='AWS_SESSION_TOKEN',
              callback=validate_aws_vars)
@click.argument('access_key_id')
def activate(access_key, secret_key, session_token, access_key_id):
    """Activate a specific access key.

    ACCESS_KEY_ID is the id of the key to activate.
    """
    mgr = Manager(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token)
    response = mgr.activate(access_key_id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Activated {access_key}".format(access_key=access_key_id))
    else:
        warn_unexpected_response('activate', response)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--access-key',
              help='AWS_ACCESS_KEY_ID to use.',
              envvar='AWS_ACCESS_KEY_ID',
              callback=validate_aws_vars)
@click.option('--secret-key',
              help=' AWS_SECRET_ACCESS_KEY to use.',
              envvar='AWS_SECRET_ACCESS_KEY',
              callback=validate_aws_vars)
@click.option('--session-token',
              help='AWS_SESSION_TOKEN to use.',
              envvar='AWS_SESSION_TOKEN',
              callback=validate_aws_vars)
@click.argument('access_key_id')
def deactivate(access_key, secret_key, session_token, access_key_id):
    """Deactivate a specific access key.

    ACCESS_KEY_ID is the id of the key to deactivate.
    """
    mgr = Manager(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token)
    response = mgr.deactivate(access_key_id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Deactivated {access_key}".format(access_key=access_key_id))
    else:
        warn_unexpected_response('deactivate', response)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--access-key',
              help='AWS_ACCESS_KEY_ID to use.',
              envvar='AWS_ACCESS_KEY_ID',
              callback=validate_aws_vars)
@click.option('--secret-key',
              help=' AWS_SECRET_ACCESS_KEY to use.',
              envvar='AWS_SECRET_ACCESS_KEY',
              callback=validate_aws_vars)
@click.option('--session-token',
              help='AWS_SESSION_TOKEN to use.',
              envvar='AWS_SESSION_TOKEN',
              callback=validate_aws_vars)
@click.argument('access_key_id')
def delete(access_key, secret_key, session_token, access_key_id):
    """Delete a specific access key.

    ACCESS_KEY_ID is the id of the key to delete.
    """
    mgr = Manager(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token)
    try:
        response = mgr.delete(access_key_id)
    except ClientError as e:
        print(e)
        raise Exit(1)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Deleted {access_key}".format(access_key=access_key_id))
    else:
        warn_unexpected_response('create', response)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--access-key',
              help='AWS_ACCESS_KEY_ID to use.',
              envvar='AWS_ACCESS_KEY_ID',
              callback=validate_aws_vars)
@click.option('--secret-key',
              help=' AWS_SECRET_ACCESS_KEY to use.',
              envvar='AWS_SECRET_ACCESS_KEY',
              callback=validate_aws_vars)
@click.option('--session-token',
              help='AWS_SESSION_TOKEN to use.',
              envvar='AWS_SESSION_TOKEN',
              callback=validate_aws_vars)
def rotate(access_key, secret_key, session_token):
    """Rotate AWS credentials.

    This will delete inactive keys before creating the new key.
    It will then deactivate the old key.
    """
    mgr = Manager(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token)
    response = mgr.rotate()

    deleted = response.get('deleted_key')
    if deleted:
        deleted_key = deleted['AccessKey']['AccessKeyId']
    else:
        deleted_key = 'N/A'
    deactivated = response.get('deactivated_key')
    if deactivated:
        deactivated_key = deactivated['AccessKey']['AccessKeyId']
    else:
        deactivated_key = 'N/A'

    key = response['new_key']['AccessKey']
    new_key = "UserName:        {}\n"\
              "AccessKeyId:     {}\n"\
              "SecretAccessKey: {}".format(key['UserName'], key['AccessKeyId'], key['SecretAccessKey'])

    msg = """Deleted Key
-----------
{deleted}

Deactivated Key
---------------
{deactivated}

New Key
-------
{new}
""".format(
        deleted=deleted_key,
        deactivated=deactivated_key,
        new=new_key,
    )
    print(msg)
