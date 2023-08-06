"""Titan Radiative Transfer Model setup."""

from pathlib import Path

from setuptools import find_packages, setup


HERE = Path(__file__).parent
README = (HERE / 'README.rst').read_text()
VERSION = (HERE / 'trtm' / '__version__.py').read_text().split("'")[1]


setup(
    name='trtm',
    version=VERSION,
    description='Titan Radiative Transfer Model package',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/seignovert/trtm',
    author='Benoit Seignovert',
    author_email='benoit.a.seignovert@jpl.nasa.gov',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    install_requires=['numpy'],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'trtm_export = trtm.cli:cli',
        ],
    },
)
