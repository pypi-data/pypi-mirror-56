# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ftlid']

package_data = \
{'': ['*']}

install_requires = \
['fasttext>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'ftlid',
    'version': '0.1.1',
    'description': 'A small and fast language identification model powered by fastText',
    'long_description': 'ftlid\n=====\n\nA simple answer to your language identification needs, powered by `fastText\n<https://fasttext.cc/>`_. It wraps the `language identification model\n<https://fasttext.cc/docs/en/language-identification.html>`_ in a small\nPython package for easier use.\n\nInstall\n-------\n\n.. code::\n\n    pip install ftlid\n\nExample\n-------\n\n.. code:: python\n\n\n    from ftlid import identify_language, load_model\n\n    # prints \'en\'\n    print(identify_language(\'Hello, how are you?\'))\n\n    # prints ([\'en\'], array([0.99987388]))\n    print(identify_language(\'Hello, how are you?\', with_prob=True))\n\n    # prints [\'en\', \'de\']\n    print(identify_language(\'And then he said "Ich liebe dich"!\', k=2))\n\n    # prints ([\'en\', \'de\'], array([0.50208992, 0.30427793]))\n    print(identify_language(\'And then he said "Ich liebe dich"!\', with_prob=True, k=2))\n\n    # if you want to use your custom model\n    print(identify_language(\'Hello, how are you?\', model_path=\'model.ftz\'))\n\n    # if you would like to pass the model yourself or prevent it from being loaded on every request\n    model = load_model(\'model.ftz\')\n    print(identify_language(\'Hello, how are you?\', model=model))\n\n\nLicense\n-------\n\nLicensed under the MIT license (see `LICENSE <./LICENSE>`_ file for more\ndetails).\n',
    'author': 'Marek Suppa',
    'author_email': 'mr@shu.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
