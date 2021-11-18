from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

# get version from __version__ variable in cargo_management/__init__.py
from cargo_management import __version__ as version

setup(
    name='cargo_management',
    version=version,
    description='Package Tracker for Local Courier Services.',
    author='Agile Shift',
    author_email='contacto@gruporeal.org',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
