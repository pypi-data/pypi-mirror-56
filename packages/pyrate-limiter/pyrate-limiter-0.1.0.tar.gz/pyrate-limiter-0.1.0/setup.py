# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyrate_limiter']

package_data = \
{'': ['*'], 'pyrate_limiter': ['engines/*']}

entry_points = \
{'console_scripts': ['et = scripts:engine_test',
                     'lint = scripts:lint',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'pyrate-limiter',
    'version': '0.1.0',
    'description': 'Python Rate-Limiter using Leaky-Bucket Algorimth Family',
    'long_description': "# Request Rate Limiter using Leaky-bucket algorimth\n\n\n## Introduction\nThis module can be used to apply rate-limit for API request, using `leaky-bucket` algorimth. User defines `window`\nduration and the limit of function calls within such interval.\n\nCurrently this package requires `Redis` to work with.\n\n## Installation\n\n``` shell\n$ pip install pyrate-limiter\n```\n\n# Usage\n\n``` python\nfrom pyrate_limiter.core import RedisBucket as Bucket, HitRate\n\n# Init bucket singleton\nbucket = Bucket('redis-url', prefix='redis-prefix')\n\n# Init rate_limiter\nlimiter = HitRate(\n    bucket,\n    capacity=10,\n    interval=60,\n)\n\n# Use as decorator\n@limiter('redis-key')\ndef call(*args, **kwargs):\n    pass\n```\n",
    'author': 'vutr',
    'author_email': 'me@vutr.io',
    'url': 'https://github.com/vutran1710/PyrateLimiter',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
