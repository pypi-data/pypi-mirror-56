# -*- coding: utf-8 -*-
"""Used to validate objects cleanly and simply."""

from setuptools import setup

setup(
    name='rdstation-client',
    version='0.0.1',
    url='https://github.com/sxslex/rdstation-client',
    download_url=(
        'https://github.com/sxslex/rdstation-client/archive/v0.0.1.tar.gz'
    ),
    author='SleX',
    author_email='sx.slex@gmail.com',
    description=(
        "Client for access API rdstation."
    ),
    keywords=['rdstation', 'api', 'client', 'rd'],
    packages=['rdstation_client'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
