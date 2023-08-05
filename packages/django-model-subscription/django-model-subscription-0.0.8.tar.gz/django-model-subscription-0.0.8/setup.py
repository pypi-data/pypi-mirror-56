# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_model_subscription', 'model_subscription']

package_data = \
{'': ['*']}

install_requires = \
['django-lifecycle>=0.3.0,<0.4.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8" or python_version >= "3.4" and python_version < "3.5"': ['typing>=3.6,<4.0']}

setup_kwargs = {
    'name': 'django-model-subscription',
    'version': '0.0.8',
    'description': 'Subscription model for a django model instance.',
    'long_description': "[![CircleCI](https://circleci.com/gh/jackton1/django-model-subscription.svg?style=shield)](https://circleci.com/gh/jackton1/django-model-subscription)\n[![Documentation Status](https://readthedocs.org/projects/django-model-subscription/badge/?version=latest)](https://django-model-subscription.readthedocs.io/en/latest/?badge=latest)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-model-subscription.svg)](https://pypi.org/project/django-model-subscription)\n[![PyPI - License](https://img.shields.io/pypi/l/django-model-subscription.svg)](https://github.com/jackton1/django-model-subscription/blob/master/LICENSE)\n[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-model-subscription.svg)](https://docs.djangoproject.com/en/2.2/releases/)\n\n![Sreenshot](https://media.giphy.com/media/IgvrR33L6S7nFgH1by/giphy.gif)\n\nhttps://python-3-patterns-idioms-test.readthedocs.io/en/latest/Observer.html\n\n\n## Table of contents\n* [Installation](#Installation)\n\n\n### Installation\n\n```bash\n$ pip install django-model-subscription\n```\n\nAdd `model_subscription` to your INSTALLED_APPS\n\n```python\nINSTALLED_APPS = [\n    ...,\n    'model_subscription',\n    ...\n]\n```\n",
    'author': 'Tonye Jack',
    'author_email': 'tonyejck@gmail.com',
    'url': 'https://django-model-subscription.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
