# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst', encoding='utf8') as freadme:
    readme = freadme.read()

with open('LICENSE', encoding='utf8') as flicense:
    lcns = flicense.read()

setup(
    name='simplejsonobject',
    version='0.1.0',
    description='A simple python object extension which can easily transform to and from json with '
                'compression support',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/mozgurbayhan/simplejsonobject',
    author='Mehmet Ozgur Bayhan',
    author_email='mozgurbayhan@gmail.com',
    license="BSD",
    keywords='json  development tracker debug',
    py_modules=['simplejsonobject'],
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://gitlab.com/mozgurbayhan/simplejsonobject/issues',
        'Funding': 'https://www.losev.org.tr/bagis/Bagis.html',
        'Say Thanks!': 'https://gitlab.com/mozgurbayhan/simplejsonobject',
        'Source': 'https://gitlab.com/mozgurbayhan/simplejsonobject'
    },

    classifiers=[

        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Database :: Front-Ends',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]

)
