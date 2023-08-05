#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup configuration"""
import os
from glob import glob
from os import path

import io
from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    """Read file specified by names path items"""
    return io.open(
        path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name="sphinx_paw",
    license="MIT",
    author="Aleksey Marin",
    author_email="asmadews@gmail.com",
    platforms="POSIX",
    version="0.4.1",
    url="https://github.com/amarin/sphinx-paw",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[
        path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')
    ],
    zip_safe=False,
    package_data={'sphinx_paw': ['locale/*/LC_MESSAGES/*.mo']},
    include_package_data=True,
    long_description=read('docs/README.rst'),
    long_description_content_type='text/x-rst',
    description="Reduce Sphinx configuration steps",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Plugins',
        'Framework :: Sphinx :: Extension',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation'
    ],
    entry_points={
        'console_scripts': [
            'make_sphinx_docs = sphinx_paw.sphinx_wrapper:main',
            'configure_docs = sphinx_paw.cmdline.init:init_docs'
        ],
        'distutils.commands': [
            'make_sphinx_docs = sphinx_paw.setup_command:Build',

        ],
    },
    setup_requires=[
        "Jinja2"
    ]

)
