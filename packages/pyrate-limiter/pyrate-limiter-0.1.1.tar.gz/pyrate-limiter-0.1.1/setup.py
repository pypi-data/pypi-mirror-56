# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyrate_limiter']

package_data = \
{'': ['*'], 'pyrate_limiter': ['engines/*']}

entry_points = \
{'console_scripts': ['lint = scripts:lint', 'test = scripts:test']}

setup_kwargs = {
    'name': 'pyrate-limiter',
    'version': '0.1.1',
    'description': 'Python Rate-Limiter using Leaky-Bucket Algorimth Family',
    'long_description': '# Request Rate Limiter using Leaky-bucket algorimth\n\n\n## Introduction\nThis module can be used to apply rate-limit for API request, using `leaky-bucket` algorimth. User defines `window`\nduration and the limit of function calls within such interval.\n\n- To hold the state of the Bucket, you can use `LocalBucket` as internal bucket.\n- To use PyrateLimiter with `Redis`,  `redis-py` is required to be installed.\n- It is also possible to use your own Bucket implementation, by extending `AbstractBucket` from `pyrate_limiter.core`\n\n\n## Project coverage\nCICD flow is not currently setup since I dont have much time, but FYI, the `coverage` is decent enought IMO...\n\n``` shell\ntests/test_leaky_bucket.py::test_bucket_overloaded PASSED\ntests/test_leaky_bucket.py::test_bucket_cooldown PASSED\ntests/test_local_engine.py::test_invalid_initials PASSED\ntests/test_local_engine.py::test_leaky_bucket_overloaded PASSED\ntests/test_local_engine.py::test_leaky_bucket_cooldown PASSED\ntests/test_local_engine.py::test_token_bucket_overloaded PASSED\ntests/test_local_engine.py::test_token_bucket_cooldown PASSED\ntests/test_redis_engine.py::test_bucket_overloaded PASSED\ntests/test_redis_engine.py::test_bucket_cooldown PASSED\ntests/test_redis_engine.py::test_normalize_redis_value PASSED\ntests/test_redis_engine.py::test_token_bucket_overloaded PASSED\ntests/test_redis_engine.py::test_token_bucket_cooldown PASSED\ntests/test_token_bucket.py::test_bucket_overloaded PASSED\ntests/test_token_bucket.py::test_bucket_cooldown PASSED\n\n---------- coverage: platform darwin, python 3.7.5-final-0 -----------\nName                                Stmts   Miss  Cover\n-------------------------------------------------------\npyrate_limiter/__init__.py              1      0   100%\npyrate_limiter/basic_algorimth.py      45      0   100%\npyrate_limiter/core.py                 63      3    95%\npyrate_limiter/engines/local.py        14      0   100%\npyrate_limiter/engines/redis.py        33      1    97%\npyrate_limiter/exceptions.py            5      0   100%\n-------------------------------------------------------\nTOTAL                                 161      4    98%\n```\n\n## Installation\n\n``` shell\n$ pip install pyrate-limiter\n```\n\n## Usage\n\n``` python\nfrom pyrate_limiter.core import TokenBucketLimiter, LeakyBucketLimiter\nfrom pyrate_limiter.engines.redis import RedisBucket\nfrom pyrate_limiter.engines.local import LocalBucket\nfrom pyrate_limiter.exceptions import BucketFullException\n\n# Init redis bucket\nbucket = RedisBucket(\'redis-url\', hash=\'some-hash\', key=\'some-key\')\n\n# Create Limiter using Token-Bucket Algorimth\n# Maximum 10 items over 60 seconds\nlimiter = TokenBucketLimiter(bucket, capacity=10, window=60)\nlimiter.queue.config(key=\'change-key\')\n# Process an item\ntry:\n    limiter.process(\'some-json-serializable-value\')\n    print(\'Item allowed to pass through\')\nexcept BucketFullException:\n    print(\'Bucket is full\')\n    # do something\n\n\n\n# Similarly, using Leaky-Bucket Algorimth\nlimiter = LeakyBucketLimiter(bucket, capacity=5, window=6)\nlimiter.queue.config(key=\'change-key\')\n# Process an item\ntry:\n    # For LeakyBucketLimiter using the similar process method, only\n    # different in naming...\n    limiter.append(\'some-json-serializable-value\')\n    print(\'Item allowed to pass through\')\nexcept BucketFullException:\n    print(\'Bucket is full\')\n    # do something\n\n\n# If using LocalBucket, the instantiation is even simpler\nbucket = LocalBucket(initial_values=some_list_type_value)\n```\n\n\n## Understanding the Algorimths\nView `tests/test_leaky_bucket.py` and `tests/test_token_bucket.py` for explaination. Documents are on the way.\n\n\n## License\nCopyright *2019* **vutr**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'vutr',
    'author_email': 'me@vutr.io',
    'url': 'https://github.com/vutran1710/PyrateLimiter',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
