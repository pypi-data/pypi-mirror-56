#!/usr/scripts/env python
from setuptools import find_packages
from distutils.core import setup
from eneel import __version__

import os
eneel_path = os.path.join(os.path.expanduser('~'), '.eneel')

package_name = "eneel"
package_version = __version__
description = """A package for fast loading av relational data"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    author="Mikael Ene",
    author_email="mikael.ene@gmail.com",
    url="https://github.com/mikaelene/eneel",
    packages=find_packages(),
    install_requires=[
        'pyodbc>=4.0.27',
        'psycopg2>=2.7.7',
        'cx-Oracle>=7.0.0',
        'PyYAML>=3.11',
        'colorama>=0.3.9',
    ],
    entry_points={
            'console_scripts': ['eneel=eneel.main:main'],
        },
    data_files = [
        (eneel_path, ['example_connections.yml']),
    ],
)
