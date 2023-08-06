# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_credentials']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['aws-credentials = aws_credentials.cli:cli']}

setup_kwargs = {
    'name': 'aws-credentials',
    'version': '0.2.0',
    'description': 'AWS credential manager',
    'long_description': '# AWS Credentials\n\nThis tool lets you easily manage AWS IAM Credentials for a user.\n\n## Usage\n```\n⇒  aws-credentials --help\nUsage: aws-credentials [OPTIONS] COMMAND [ARGS]...\n\n  CLI utility for managing access keys.\n\nOptions:\n  -v, --verbose  Increase the verbosity of messages: "-v" for normal output,\n                 and "-vv" for more verbose output.\n  -h, --help     Show this message and exit.\n\nCommands:\n  activate    Activate a specific access key.\n  create      Create a new access key.\n  deactivate  Deactivate a specific access key.\n  delete      Delete a specific access key.\n  list        List access keys.\n  rotate      Rotate AWS credentials.\n```\n\n**activate**\n```\n⇒  aws-credentials activate --help\nUsage: aws-credentials activate [OPTIONS] ACCESS_KEY_ID\n\n  Activate a specific access key.\n\n  ACCESS_KEY_ID is the id of the key to activate.\n\nOptions:\n  --access-key TEXT     AWS_ACCESS_KEY_ID to use.\n  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.\n  --session-token TEXT  AWS_SESSION_TOKEN to use.\n  -h, --help            Show this message and exit.\n```\n\n**create**\n```\n⇒  aws-credentials create --help\nUsage: aws-credentials create [OPTIONS]\n\n  Create a new access key.\n\nOptions:\n  --access-key TEXT     AWS_ACCESS_KEY_ID to use.\n  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.\n  --session-token TEXT  AWS_SESSION_TOKEN to use.\n  -h, --help            Show this message and exit.\n```\n\n**deactivate**\n```\n⇒  aws-credentials deactivate --help\nUsage: aws-credentials deactivate [OPTIONS] ACCESS_KEY_ID\n\n  Deactivate a specific access key.\n\n  ACCESS_KEY_ID is the id of the key to deactivate.\n\nOptions:\n  --access-key TEXT     AWS_ACCESS_KEY_ID to use.\n  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.\n  --session-token TEXT  AWS_SESSION_TOKEN to use.\n  -h, --help            Show this message and exit.\n```\n\n**delete**\n```\n⇒  aws-credentials delete --help\nUsage: aws-credentials delete [OPTIONS] ACCESS_KEY_ID\n\n  Delete a specific access key.\n\n  ACCESS_KEY_ID is the id of the key to delete.\n\nOptions:\n  --access-key TEXT     AWS_ACCESS_KEY_ID to use.\n  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.\n  --session-token TEXT  AWS_SESSION_TOKEN to use.\n  -h, --help            Show this message and exit.\n```\n\n**list**\n```\n⇒  aws-credentials list --help\nUsage: aws-credentials list [OPTIONS]\n\n  List access keys.\n\nOptions:\n  --access-key TEXT     AWS_ACCESS_KEY_ID to use.\n  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.\n  --session-token TEXT  AWS_SESSION_TOKEN to use.\n  -h, --help            Show this message and exit.\n```\n\n**rotate**\n```\n⇒  aws-credentials rotate --help\nUsage: aws-credentials rotate [OPTIONS]\n\n  Rotate AWS credentials.\n\n  This will delete inactive keys before creating the new key. It will then\n  deactivate the old key.\n\nOptions:\n  --access-key TEXT     AWS_ACCESS_KEY_ID to use.\n  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.\n  --session-token TEXT  AWS_SESSION_TOKEN to use.\n  -h, --help            Show this message and exit.\n```\n',
    'author': 'Paul Robertson',
    'author_email': 't.paulrobertson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/perobertson/aws-credentials',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
