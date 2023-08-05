# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sd_fail_notify']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'requests>=2.22,<3.0',
 'toml>=0.10.0,<0.11.0',
 'twilio>=6.33,<7.0']

entry_points = \
{'console_scripts': ['sd-fail-notify = sd_fail_notify.main:cli']}

setup_kwargs = {
    'name': 'sd-fail-notify',
    'version': '19.11.1',
    'description': 'Send a text message when a systemd process fails',
    'long_description': '# Systemd Failure Notifier\nThis is a simple command utility designed to be run on the failure of a systemd unit.\n\n## Usage\n`sd-fail-notify <unit-name>`\n \n It is meant to be used with the `%i` unit name option passed in a systemd OnFailure dependency\n \n ## Supported Providers\n \n ### Twilio\n \n Required configuration: from, to, account, token. See example config for details.\n',
    'author': 'Rick Henry',
    'author_email': 'rickhenry@rickhenry.dev',
    'url': 'https://github.com/rickh94/sd_fail_notify.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
