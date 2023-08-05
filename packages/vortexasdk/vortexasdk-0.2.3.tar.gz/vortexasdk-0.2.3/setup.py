# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['vortexasdk', 'vortexasdk.api', 'vortexasdk.endpoints']

package_data = \
{'': ['*']}

install_requires = \
['flatten-dict==0.2.0', 'jsons==1.0.0', 'pandas==0.25.2', 'requests==2.22.0']

setup_kwargs = {
    'name': 'vortexasdk',
    'version': '0.2.3',
    'description': 'Vorexa DataScience SDK (Software Developlent Kit)',
    'long_description': '# VortexaSDK\n\n[![CircleCI](https://circleci.com/gh/V0RT3X4/python-sdk.svg?style=svg)](https://circleci.com/gh/V0RT3X4/python-sdk)\n\nThe VortexaSDK is Vortexa\'s Software Development Kit (SDK) for Python, which allows\nData Scientists, Analysts and Developers to query [Vortexa\'s API](https://docs.vortexa.com)\n\n\n\n## Quick Start\n\n##### Installation\n\n```bash\n$ pip install vortexasdk\n```\n\n##### Authentication\n\nSet your `VORTEXA_API_KEY` environment variable, that\'s all.\n\n##### Example\n\n```python\n>>> from vortexasdk import CargoMovements\n>>> df = CargoMovements() \\\n        .search(filter_time_min="2019-08-01T00:00:00.000Z", filter_time_max="2019-08-01T00:15:00.000Z")\\\n        .to_df()\n```\n\n\n## Documentation\n\nRead the documentation at [VortexaSDK Docs](https://v0rt3x4.github.io/python-sdk/)\n\n## Contributing\n\nWe welcome contributions! Please read our [Contributing Guide](https://github.com/V0RT3X4/python-sdk/blob/master/CONTRIBUTING.md) for ways to offer feedback and contributions.\n\n## Glossary\n\nThe Glossary can be found at [Vortexa API Documentation](https://docs.vortexa.com)\n\nThis outlines key terms, functions and assumptions aimed at\nhelping to extract powerful findings from our data.\n\n',
    'author': 'Vortexa Developers',
    'author_email': 'developers@vortexa.com',
    'url': 'https://github.com/V0RT3X4/python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
