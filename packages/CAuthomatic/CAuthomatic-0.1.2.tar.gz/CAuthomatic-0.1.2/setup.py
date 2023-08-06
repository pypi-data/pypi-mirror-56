# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

from authomatic import six


setup(
    name='CAuthomatic',
    version='0.1.2',
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rst']},
    author='Hai Bui',
    author_email='hai.bui@kkday.com',
    description=('Authorization / authentication client library for '
                 'Python web applications'),
    long_description=open('README.rst').read(),
    keywords='authorization authentication oauth openid',
    url='https://github.com/hai-bui-kkday/authomatic',
    license='MIT',
    extras_require={
        'OpenID': ['python3-openid' if six.PY3 else 'python-openid'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: '
        'CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
