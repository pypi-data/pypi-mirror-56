"""The setup script."""

import os
from setuptools import setup, find_packages
import sys

import symbol_please

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    'colorlog>=4.0.2',
    'python-dateutil>=2.8.0',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

if sys.platform == 'linux':
    if os.getuid() == 0:
        share_dir = os.getenv('XDG_DATA_DIRS', '/usr/local/share/:/usr/share/').split(':', 1)[0]
    else:
        share_dir = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
    data_files = [
        (os.path.join(share_dir, 'applications'), ['data/info.armills.SymbolPlease.desktop']),
        (os.path.join(share_dir, 'pixmaps'), ['data/symbol_please.png']),
    ]
else:
    data_files = []

setup(
    author=symbol_please.__author__,
    author_email=symbol_please.__email__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Symbol Please is a visual log parsing helper for Project 1999",
    entry_points={
        'console_scripts': [
            'symbol_please=symbol_please.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    include_package_data=True,
    keywords='symbol_please',
    name='symbol_please',
    packages=find_packages(include=['symbol_please']),
    package_data={'symbol_please': ['data/spell_data.json']},
    data_files = data_files,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/armills/symbol_please',
    version=symbol_please.__version__,
    zip_safe=False,
)
