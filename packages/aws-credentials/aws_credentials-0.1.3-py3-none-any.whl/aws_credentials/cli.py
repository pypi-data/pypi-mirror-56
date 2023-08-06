import logging

import click
from botocore.exceptions import ClientError
from click.exceptions import Exit

from .manager import Manager

logger = logging.getLogger(__name__)
pass_manager = click.make_pass_decorator(Manager)


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
    if value:
        return value
    raise click.BadParameter('cannot be blank.')


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


@click.group()
@click.option('--access_key',
              help='AWS_ACCESS_KEY_ID to use', prompt='Access Key',
              envvar='AWS_ACCESS_KEY_ID', callback=validate_aws_vars)
@click.option('--secret_key',
              help=' AWS_SECRET_ACCESS_KEY to use', prompt='Secret Key',
              envvar='AWS_SECRET_ACCESS_KEY', callback=validate_aws_vars)
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, access_key, secret_key, verbose):
    """CLI utility for managing access keys."""
    if verbose == 1:
        init_logging(logging.INFO)
    elif verbose == 2:
        init_logging(logging.DEBUG)
    else:
        init_logging(logging.WARNING)
    ctx.obj = Manager(access_key, secret_key)


@cli.command()
@pass_manager
def list(mgr):
    keys = mgr.keys()
    headers = 'AccessKeyId', 'Status', 'CreateDate'
    print("{:20} {:8} {}".format(*headers))
    for key in keys:
        print("{} {:8} {}".format(key['AccessKeyId'], key['Status'], key['CreateDate']))


@cli.command()
@pass_manager
def create(mgr):
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


@cli.command()
@pass_manager
@click.argument('access_key')
def activate(mgr, access_key):
    response = mgr.activate(access_key)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Activated {access_key}".format(access_key=access_key))
    else:
        warn_unexpected_response('activate', response)


@cli.command()
@pass_manager
@click.argument('access_key')
def deactivate(mgr, access_key):
    response = mgr.deactivate(access_key)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Deactivated {access_key}".format(access_key=access_key))
    else:
        warn_unexpected_response('deactivate', response)


@cli.command()
@pass_manager
@click.argument('access_key')
def delete(mgr, access_key):
    try:
        response = mgr.delete(access_key)
    except ClientError as e:
        print(e)
        raise Exit(1)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Deleted {access_key}".format(access_key=access_key))
    else:
        warn_unexpected_response('create', response)


@cli.command()
@pass_manager
def rotate(mgr):
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
