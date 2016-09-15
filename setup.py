"""
interfax
========

"""

import ast
import re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('interfax/__init__.py', 'rb') as f:
    version = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(version).group(1)))

with open('README.rst', 'rb') as f:
    README = f.read().decode('utf-8')

setup(
    name='interfax',
    version=version,
    url='http://github.com/interfax/interfax-python',
    license='MIT',
    author='Daniel Knell',
    author_email='contact@danielknell.co.uk',
    description='InterFAX python library',
    long_description=README,
    packages=['interfax'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'cached-property>=1.3.0',
        'inflection>=0.3.1',
        'python-magic>=0.4.12',
        'requests>=2.11.1',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
