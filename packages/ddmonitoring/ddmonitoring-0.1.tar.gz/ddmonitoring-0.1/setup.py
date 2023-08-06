#!/usr/bin/env python

PROJECT = 'ddmonitoring'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

setup(
    name=PROJECT,
    version=VERSION,

    description='CLI Take Home Project for Datadog',

    author='Guillaume Brizolier',
    author_email='gbrizolier@gmail.com',

    url='https://github.com/chaoticdenim/dd-monitoring',
    download_url='https://github.com/chaoticdenim/dd-monitoring/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff', "asyncio", "requests", "apscheduler", "numpy", "asciimatics", "jsonschema", "tqdm"],

    namespace_packages=[],
    packages=['ddmonitoring'],
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'ddmonitoring = ddmonitoring.main:main'
        ],
        'dd.monitoring': [
            'run = ddmonitoring.run:Run',
        ],
    },

    zip_safe=False,
)
