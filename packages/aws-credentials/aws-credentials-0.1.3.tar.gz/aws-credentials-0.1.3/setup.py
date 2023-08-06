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
    'version': '0.1.3',
    'description': 'AWS credential manager',
    'long_description': '# AWS Credentials\n\nThis tool lets you easily manage AWS IAM Credentials for a user.\n\n## Usage\n```\n⇒  aws-credentials --help\nUsage: aws-credentials [OPTIONS] COMMAND [ARGS]...\n\n  CLI utility for managing access keys.\n\nOptions:\n  --access_key TEXT  AWS_ACCESS_KEY_ID to use\n  --secret_key TEXT  AWS_SECRET_ACCESS_KEY to use\n  -v, --verbose\n  --help             Show this message and exit.\n\nCommands:\n  activate\n  create\n  deactivate\n  delete\n  list\n  rotate\n```\n\n**activate**\n```\n⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials activate --help\nUsage: aws-credentials activate [OPTIONS] ACCESS_KEY\n\nOptions:\n  --help  Show this message and exit.\n```\n\n**create**\n```\n⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials create --help\nUsage: aws-credentials create [OPTIONS]\n\nOptions:\n  --help  Show this message and exit.\n```\n\n**deactivate**\n```\n⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials deactivate --help\nUsage: aws-credentials deactivate [OPTIONS] ACCESS_KEY\n\nOptions:\n  --help  Show this message and exit.\n```\n\n**delete**\n```\n⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials delete --help\nUsage: aws-credentials delete [OPTIONS] ACCESS_KEY\n\nOptions:\n  --help  Show this message and exit.\n```\n\n**list**\n```\n⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials list --help\nUsage: aws-credentials list [OPTIONS]\n\nOptions:\n  --help  Show this message and exit.\n```\n\n**rotate**\n```\n⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials rotate --help\nUsage: aws-credentials rotate [OPTIONS]\n\nOptions:\n  --help  Show this message and exit.\n```\n',
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
