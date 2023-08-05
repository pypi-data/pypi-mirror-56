# -*- coding: utf-8 -*-
from distutils.dist import DistributionMetadata
from os import mkdir
from os import path
from sys import stderr
from sys import stdout


def exit_with_error(error_text):
    """Write text to stderr and exit"""
    stderr.write(error_text+'\n')
    exit(1)


def get_project_settings():
    """Get project settings"""
    setup_file = path.join(path.curdir, 'setup.py')
    if not path.exists(setup_file):
        raise FileNotFoundError()

    metadata = DistributionMetadata(setup_file)
    return metadata


def init_docs():
    """Init sphinx docs folder and configuration files"""

    try:
        meta = get_project_settings()
    except FileNotFoundError:
        exit_with_error(
            "No setup.py found in current path. Configure your project first"
        )

    current_path = path.curdir
    target_path = path.join(current_path, 'docs')
    if not path.exists(target_path):
        stdout.write("Creating docs/")
        mkdir(target_path)

    if meta.name is None:
        exit_with_error("Cant detect package name")

    stdout.write(f"Configure {meta.name} documentation")


