# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Index Sync is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Invenio digital library framework."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('index_sync', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='index-sync',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='index-sync Invenio',
    license='MIT',
    author='CERN',
    author_email='info@index-sync.com',
    url='https://github.com/index-sync/index-sync',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'index-sync = invenio_app.cli:cli',
        ],
        'flask.commands': [
            'demo = index_sync.cli:demo'
        ],
        'invenio_base.apps': [
            'index_sync_records = index_sync.records:IndexSync',
        ],
        'invenio_base.blueprints': [
            'index_sync = index_sync.theme.views:blueprint',
            'index_sync_records = index_sync.records.views:blueprint',
        ],
        'invenio_assets.webpack': [
            'index_sync_theme = index_sync.theme.webpack:theme',
        ],
        'invenio_config.module': [
            'index_sync = index_sync.config',
        ],
        'invenio_i18n.translations': [
            'messages = index_sync',
        ],
        'invenio_base.api_apps': [
            'index_sync = index_sync.records:IndexSync',
         ],
        'invenio_jsonschemas.schemas': [
            'index_sync = index_sync.records.jsonschemas'
        ],
        'invenio_search.mappings': [
            'records = index_sync.records.mappings'
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
