#!/usr/bin/env python

import os.path
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.dirname(__file__))


setup(
    name="django-states3",
    version='3.0.0',
    url='https://github.com/ulamlabs/django-states3',
    license='BSD',
    description="State machine for django models",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Ulam Labs',  # Jonathan Slenders, Gert van Gool, Maarten Timmerman, Steven (rh0dium), Unleashed NV
    author_email='contact@ulam.io',
    packages=find_packages('.', exclude=['test_proj',]),
    test_suite='test_proj.runtests.main',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
