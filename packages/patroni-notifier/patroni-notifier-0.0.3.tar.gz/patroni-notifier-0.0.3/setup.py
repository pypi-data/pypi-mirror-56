# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['patroni_notifier']

package_data = \
{'': ['*'], 'patroni_notifier': ['templates/*']}

install_requires = \
['boto3>=1.10.12,<2.0.0',
 'click>=7.0,<8.0',
 'jinja2>=2.10.3,<3.0.0',
 'python-consul>=1.1.0,<2.0.0',
 'pyyaml>=5.1,<6.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['patroni-notify = patroni_notifier.core:patroni_notify']}

setup_kwargs = {
    'name': 'patroni-notifier',
    'version': '0.0.3',
    'description': 'Patoni notification system using jinja2 templates',
    'long_description': '# Patroni Notifier\n\n![](https://github.com/jaredvacanti/patroni-notifier/workflows/Publish%20to%20PyPI/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/patroni-notifier?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/patroni-notifier?style=flat-square)\n\nThis is a simple command line program to send templated emails from AWS SES in response\nto Patroni database events.\n\n## Installation\n\n```\npip install patroni-notifier\n```\n\n## Usage\n\nSystem-wide configurations are done in the `patroni.yml` file required for \nPatroni operations. You can further specify a config file location using \n`--config` as a command line option, which defaults to `/config/patroni.yml`.\n\n**Required Settings in patroni.yml**\n```\nemail_sender: John Doe <example.com>\nemail_recipient: test@example.com\nemail_subject: Sample Subject\n```\n\nPatroni will send a notification on role change by invoking callback scripts \nto run on certain actions. Patroni will pass the action, role and cluster name.\n\nThe program is then run like `patroni-notify ACTION ROLE CLUSTER_NAME`. Add this\nsnippet to your `patroni.yml`:\n\n```\ncallbacks:\n  on_reload: /usr/local/bin/patroni-notify\n  on_restart: /usr/local/bin/patroni-notify\n  on_role_change: /usr/local/bin/patroni-notify\n  on_start: /usr/local/bin/patroni-notify\n  on_stop: /usr/local/bin/patroni-notify\n```\n### Authentication\n\nCurrently emails are sent using Amazon SES. Authenication can use IAM roles\nor you can place a `aws.env` in your home directory with credentials.\n\n## Tests\n\n```\npoetry run tox\n```\n\n## License\n\nMIT License\n\nCopyright (c) 2019\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'Jared Vacanti',
    'author_email': 'jaredvacanti@gmail.com',
    'url': 'https://github.com/jaredvacanti/patroni-notifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
