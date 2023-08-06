from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyStratum-MySQL',

    version='0.10.17',

    description='A stored procedure and function loader and wrapper generator for MySQL & MariaDB',
    long_description=long_description,

    url='https://github.com/SetBased/py-stratum-mysql',

    author='Set Based IT Consultancy',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Installation/Setup',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='stored routines, wrapper, loader, MySQL, MariaDB',

    packages=find_packages(exclude=['build', 'test']),

    install_requires=['pystratum>=0.10.22'],
)
