# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['data_extractor']

package_data = \
{'': ['*']}

install_requires = \
['cssselect>=1.0.3,<2.0.0',
 'jsonpath-rw-ext>=1.2,<2.0',
 'jsonpath-rw>=1.4.0,<2.0.0',
 'lxml>=4.3.0,<5.0.0']

extras_require = \
{'docs': ['sphinx>=2.2,<3.0'],
 'linting': ['black>=19.3b0,<20.0',
             'flake8>=3.7.8,<4.0.0',
             'isort>=4.3.21,<5.0.0',
             'mypy>=0.730,<0.731',
             'pytest>=5.2.0,<6.0.0',
             'doc8>=0.8.0,<0.9.0',
             'pygments>=2.4,<3.0',
             'flake8-bugbear>=19.8,<20.0',
             'blacken-docs>=1.3,<2.0'],
 'test': ['pytest>=5.2.0,<6.0.0', 'pytest-cov>=2.7.1,<3.0.0']}

setup_kwargs = {
    'name': 'data-extractor',
    'version': '0.5.3',
    'description': 'Combine XPath, CSS Selectors and JSONPath for Web data extracting.',
    'long_description': '==============\nData Extractor\n==============\n\n|license| |Pypi Status| |Python version| |Package version| |PyPI - Downloads|\n|GitHub last commit| |Code style: black| |Build Status| |codecov|\n|Documentation Status|\n\nCombine **XPath**, **CSS Selectors** and **JSONPath** for Web data extracting.\n\nQuickstarts\n<<<<<<<<<<<\n\nInstallation\n~~~~~~~~~~~~\n\nInstall the stable version from PYPI.\n\n.. code-block:: shell\n\n    pip install data-extractor\n\nOr install the latest version from Github.\n\n.. code-block:: shell\n\n    pip install git+https://github.com/linw1995/data_extractor.git@master\n\nUsage\n~~~~~\n\n.. code-block:: python3\n\n    from data_extractor import Field, Item, JSONExtractor\n\n\n    class Count(Item):\n        followings = Field(JSONExtractor("countFollowings"))\n        fans = Field(JSONExtractor("countFans"))\n\n\n    class User(Item):\n        name_ = Field(JSONExtractor("name"), name="name")\n        age = Field(JSONExtractor("age"), default=17)\n        count = Count()\n\n\n    assert User(JSONExtractor("data.users[*]"), is_many=True).extract(\n        {\n            "data": {\n                "users": [\n                    {\n                        "name": "john",\n                        "age": 19,\n                        "countFollowings": 14,\n                        "countFans": 212,\n                    },\n                    {\n                        "name": "jack",\n                        "description": "",\n                        "countFollowings": 54,\n                        "countFans": 312,\n                    },\n                ]\n            }\n        }\n    ) == [\n        {"name": "john", "age": 19, "count": {"followings": 14, "fans": 212}},\n        {"name": "jack", "age": 17, "count": {"followings": 54, "fans": 312}},\n    ]\n\nChangelog\n<<<<<<<<<\n\nv0.5.3\n~~~~~~\n\n- 6a26be5 Chg:Wrap the single return value as a list\n- 0b63927 Fix:Item can not extract the data is list type\n- 9deeb5f Chg:Update poetry.lock\n\n\n.. |license| image:: https://img.shields.io/github/license/linw1995/data_extractor.svg\n    :target: https://github.com/linw1995/data_extractor/blob/master/LICENSE\n\n.. |Pypi Status| image:: https://img.shields.io/pypi/status/data_extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |Python version| image:: https://img.shields.io/pypi/pyversions/data_extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |Package version| image:: https://img.shields.io/pypi/v/data_extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/data-extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/linw1995/data_extractor.svg\n    :target: https://github.com/linw1995/data_extractor\n\n.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. |Build Status| image:: https://travis-ci.org/linw1995/data_extractor.svg?branch=master\n    :target: https://travis-ci.org/linw1995/data_extractor\n\n.. |codecov| image:: https://codecov.io/gh/linw1995/data_extractor/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/linw1995/data_extractor\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/data-extractor/badge/?version=latest\n    :target: https://data-extractor.readthedocs.io/en/latest/?badge=latest\n',
    'author': 'linw1995',
    'author_email': 'linw1995@icloud.com',
    'url': 'https://github.com/linw1995/data_extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
