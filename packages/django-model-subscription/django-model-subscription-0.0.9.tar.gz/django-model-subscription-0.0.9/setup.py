# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_model_subscription', 'model_subscription']

package_data = \
{'': ['*']}

install_requires = \
['django-lifecycle>=0.3.0,<0.4.0', 'typing_extensions>=3.7,<4.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8" or python_version >= "3.4" and python_version < "3.5"': ['typing>=3.6,<4.0']}

setup_kwargs = {
    'name': 'django-model-subscription',
    'version': '0.0.9',
    'description': 'Subscription model for a django model instance.',
    'long_description': "[![CircleCI](https://circleci.com/gh/jackton1/django-model-subscription.svg?style=shield)](https://circleci.com/gh/jackton1/django-model-subscription)\n[![Documentation Status](https://readthedocs.org/projects/django-model-subscription/badge/?version=latest)](https://django-model-subscription.readthedocs.io/en/latest/?badge=latest)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-model-subscription.svg)](https://pypi.org/project/django-model-subscription)\n[![PyPI - License](https://img.shields.io/pypi/l/django-model-subscription.svg)](https://github.com/jackton1/django-model-subscription/blob/master/LICENSE)\n[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-model-subscription.svg)](https://docs.djangoproject.com/en/2.2/releases/)\n\n[django-model-subscription](https://django-model-subscription.readthedocs.io/en/latest/installation.html)\n\n![Sreenshot](https://media.giphy.com/media/IgvrR33L6S7nFgH1by/giphy.gif)\n\nhttps://python-3-patterns-idioms-test.readthedocs.io/en/latest/Observer.html\n\n\n## Table of contents\n* [Motivation](#Motivation)\n* [Installation](#Installation)\n* [Usage](#Usage)\n* [Decorators](#Decorators)\n* [Setup Subscribers using App.ready](#setup-subscribers-using-appready-recomended)\n* [Setup Subscribers with auto discovery](#setup-subscribers-using-auto-discovery)\n\n\n### Motivation\n\n- Extending django models using Observer Pattern.\n- Decouple Business logic from Models.save\n- Support for bulk actions (Not available using django signals.)\n- Use noop subscribers when `settings.SUBSCRIPTION_RUN_EXTERNAL` is `False` \n  which prevents having to mock external service subscribers in testing, local development environments.\n- Show changes to the instance after it has been updated i.e diff's the initial state and the \ncurrent state.\n\n![Screenshot](Subscriber.png)\n\n\n### Installation\n\n```bash\n$ pip install django-model-subscription\n```\n\nAdd `model_subscription` to your INSTALLED_APPS\n\n```python\nINSTALLED_APPS = [\n    ...,\n    'model_subscription',\n    ...\n]\n```\n\n\n\n\n### Usage\n\n#### Creating subscribers.\n\n- Using `OperationType`\n\n```python\nimport logging\nfrom model_subscription.decorators import subscribe\nfrom model_subscription.constants import OperationType\n\nlog = logging.getLogger(__name__)\n\n@subscribe(OperationType.CREATE, TestModel)\ndef handle_create(instance):\n    log.debug('Created {}'.format(instance.name))\n\n\n```\n\n- Using `create_subscription` directly (succinct version).\n\n```python\n\nimport logging\nfrom model_subscription.decorators import create_subscription\n\nlog = logging.getLogger(__name__)\n\n@create_subscription(TestModel)\ndef handle_create(instance):\n    log.debug('Created {}'.format(instance.name))\n\n\n```\n\n\n### Decorators\n\n* `subscribe`: Explicit (Requires a valid OperationType).\n\n\n#### (Create, Update, Delete) operations. \n\n* `create_subscription`: Subscribes to create operation i.e a new instance.\n\n```python\n@create_subscription(TestModel)\ndef handle_create(instance):\n    log.debug('1. Created {}'.format(instance.name))\n```\n\n* `update_subscription`: Subscribes to updates also includes (`changed_data`).\n```python\n@update_subscription(TestModel)\ndef handle_update(instance, changed_data):\n    log.debug('Updated {} {}'.format(instance.name, changed_data))\n```\n\n\n* `delete_subscription`: Subscribes to delete operation: \n\n> NOTE: The instance.pk is already set to None.\n\n```python\n@delete_subscription(TestModel)\ndef handle_delete(instance):\n    log.debug('Deleted {}'.format(instance.name))\n```\n\n#### (Bulk Create, Bulk Update, Bulk Delete) operations. \n\n* `bulk_create_subscription`: Subscribe to bulk create operations.\n\n```python\n\n@bulk_create_subscription(TestModel)\ndef handle_bulk_create(instances):\n    for instance in instances:\n        log.debug('Bulk Created {}'.format(instance.name))\n\n```\n\n\n* `bulk_update_subscription`: Subscribe to bulk update operations.\n\n```python\n@bulk_update_subscription(TestModel)\ndef handle_bulk_update(instances):\n    for instance in instances:\n        log.debug('Updated {}'.format(instance.name))\n```\n\n\n* `bulk_delete_subscription`: Subscribe to bulk delete operations.\n\n```python\n\n@bulk_delete_subscription(TestModel)\ndef handle_bulk_delete(instances):\n    for instance in instances:\n        log.debug('Deleted {}'.format(instance.name))\n\n```\n\n\n### Setup Subscribers using App.ready `(Recomended)`. \n\n\nUpdate you `apps.py`\n\n\n```python\n\nfrom django.apps import AppConfig\n\n\nclass MyAppConfig(AppConfig):\n    name = 'myapp'\n\n    def ready(self):\n        from myapp import subscriptions\n\n```\n\n\n\n### Setup Subscribers using auto discovery.\n\nBy default the `settings.SUBSCRIPTION_AUTO_DISCOVER` is set to `False`.\n\nTo use auto discovery this is not recommended as it would notify the subscribers \nwherever the model is used i.e IPython notebook, external scripts.\n\nIn your `settings.py` add\n\n```python\n\nSUBSCRIPTION_AUTO_DISCOVER = True\n\n```\n\n#### Setting up the `SUBSCRIPTION_MODULE`\n\n> NOTE: This is only required when ``SUBSCRIPTION_AUTO_DISCOVER = True``\n\n```python\n\nSUBSCRIPTION_MODULE  = 'subscription' \n\n```\n\nTODO's\n- Supporting field level subscriptions.\n- Support class based subscribers which implements `__call__`\n- Extend to include custom OperationType.\n",
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
