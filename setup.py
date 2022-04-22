
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='stock_exchange',
    version='0.1.0',
    description="A simple stock exchange python CLI app",
    author="Eduard Paul",
    author_email='paul.ev@phystech.edu',
    url='https://github.com/EdwardPaul/stock_exchange',
    packages=[
        'stock_exchange',
        'stock_exchange.domain',
        'stock_exchange.shared',
        'stock_exchange.use_cases',
        'stock_exchange.repository'
    ],
    package_dir={'stock_exchange':
                 'stock_exchange'},
    include_package_data=True,
    zip_safe=False,
    keywords='stock_exchange',
    test_suite='tests',
)
