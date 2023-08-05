'''
copied and modified from https://github.com/pypa/sampleproject
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import re

long_description = open('README.txt').read()

version = '1.0.0'

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='iqra',
    version=version,
    description='iqra, a library management program.',
    long_description=long_description,
    url='https://github.com/alghafli/iqra',
    author='Mohammad Alghafli',
    author_email='thebsom@gmail.com',
    keywords='library management program',
    packages=find_packages(),
    install_requires=['sqlalchemy', 'appdirs', 'codi'],
    extras_require={
        'cairo': ['pycairo'],
    },
    include_package_data=True,
    entry_points={
        'iqra.commands': [
            'new=iqra.commands:new',
            'edit=iqra.commands:edit',
            'delete=iqra.commands:delete',
            'list=iqra.commands:list_',
            'file=iqra.commands:file',
            'commit=iqra.commands:commit',
            'rollback=iqra.commands:rollback',
            'echo=iqra.commands:echo',
            'backup=iqra.commands:backup',
            'lsbackup=iqra.commands:lsbackup',
            'restore=iqra.commands:restore',
            'thumb=iqra.commands:thumb [cairo]',
        ],
        'iqra.plugins': [
            'importdb=iqra.plugins:importdb',
            'exportdb=iqra.plugins:exportdb',
            'stickers=iqra.plugins:stickers [cairo]',
        ]
    },

    #project_urls={
    #    'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #    'Funding': 'https://donate.pypi.org',
    #    'Say Thanks!': 'http://saythanks.io/to/example',
    #    'Source': 'https://github.com/pypa/sampleproject/',
    #},
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],
)
