'''
copied and modified from https://github.com/pypa/sampleproject
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import re

long_description = open('README.txt').read()

version = '1.2'

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='giqra',
    version=version,
    description='giqra, a gui for iqra.',
    long_description=long_description,
    url='https://github.com/alghafli/giqra',
    author='Mohammad Alghafli',
    author_email='thebsom@gmail.com',
    keywords='library management program gui iqra',
    packages=find_packages(),
    install_requires=['iqra', 'pygobject>=3.20'],
    extras_require={},
    include_package_data=True,
    entry_points={},

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
