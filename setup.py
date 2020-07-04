# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in parcel_management/__init__.py
from parcel_management import __version__ as version

setup(
	name='parcel_management',
	version=version,
	description='Track parcels(Packages) across multiple carriers.',
	author='Agile Shift',
	author_email='contacto@agileshift.io',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
