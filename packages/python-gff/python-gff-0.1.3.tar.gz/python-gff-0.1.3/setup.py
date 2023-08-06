# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['__init__']
setup_kwargs = {
    'name': 'python-gff',
    'version': '0.1.3',
    'description': 'A more general GFF/GTF parser',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
