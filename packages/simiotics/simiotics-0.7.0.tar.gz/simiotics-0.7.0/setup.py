from setuptools import find_packages, setup

import simiotics

long_description = ''
with open('README.md') as ifp:
    long_description = ifp.read()

setup(
    name='simiotics',
    version=simiotics.VERSION,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.22.0,<3.0.0',
    ],
    description='Simiotics Python Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Neeraj Kashyap',
    author_email='neeraj@simiotics.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'simiotics = simiotics.cli:main'
        ],
    },
)
