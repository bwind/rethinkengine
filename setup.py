import os
from setuptools import setup

setup(
    name='rethinkengine',
    version='0.1.0',
    author='Bas Wind',
    author_email='mailtobwind@gmail.com',
    description='RethinkDB Object-Document Mapper',
    license='BSD',
    keywords='rethinkdb object-document mapper',
    url='https://github.com/bwind/rethinkengine',
    download_url='https://pypi.python.org/pypi/Propeller',
    packages=['rethinkengine'],
    include_package_data=True,
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'rethinkdb==1.9.0-0',
        'ordereddict==1.1',
    ],
)
