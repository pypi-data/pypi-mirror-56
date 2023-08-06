"""Titan Radiative Transfer Model setup."""

from setuptools import setup


with open('requirements.txt', 'r') as f:
    lines = f.read().splitlines()
    requirements = [line if '#egg=' not in line else
                    line.split('#egg=', 1)[1]
                    for line in lines]
    links = [line.split()[-1] for line in lines if '#egg=' in line]


with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='trtm',
    version='0.1',
    description='Titan Radiative Transfer Model package',
    author='Benoit Seignovert',
    author_email='benoit.a.seignovert@jpl.nasa.gov',
    url='https://github.com/seignovert/trtm',
    python_requires='>=3.6',
    license='MIT',
    packages=['trtm'],
    long_description=long_description,
    install_requires=requirements,
    dependency_links=links,
    entry_points={
        'console_scripts': [
            'trtm_export = trtm.cli:cli',
        ],
    },
)
