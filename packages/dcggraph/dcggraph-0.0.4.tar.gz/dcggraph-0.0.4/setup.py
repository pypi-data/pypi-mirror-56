"""A setuptools based setup module"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dcggraph',
    version='0.0.4',
    description='Directed Cyclic Graph Utilities for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='directed cyclic graph traversal',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    packages=["dcggraph"],
    python_requires='>=3.6',
    install_requires=["typing"],
    entry_points={},

    url='https://github.com/ssteffl/python-dcggraph',
    author='Sam Steffl',
    author_email='sam@ssteffl.com',
    project_urls={
        'Bug Reports': 'https://github.com/ssteffl/python-dcggraph',
        'Source': 'https://github.com/ssteffl/python-dcggraph',
    },
)
