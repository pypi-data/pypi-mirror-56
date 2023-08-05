"""A setuptools based setup module"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hilite_syntax',
    version='0.0.4',
    description='Framework for generating editor syntax files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='hilite hilight syntax editor',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    packages=["hilite_syntax"],
    python_requires='>=3.6',
    install_requires=["dcggraph", "lark-parser"],
    scripts=["./bin/hilite_syntax"],

    url='https://github.com/ssteffl/python-hilite-syntax',
    author='Sam Steffl',
    author_email='sam@ssteffl.com',
    project_urls={
        'Bug Reports': 'https://github.com/ssteffl/python-hilite-syntax',
        'Source': 'https://github.com/ssteffl/python-hilite-syntax',
    },
)
