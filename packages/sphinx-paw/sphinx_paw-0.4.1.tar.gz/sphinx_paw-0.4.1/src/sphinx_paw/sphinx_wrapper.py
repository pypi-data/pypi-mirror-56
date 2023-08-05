# -*- coding: utf-8 -*-
import codecs
from os import path, rename

conf_py_template="""# -*- coding: utf-8 -*-
\"\"\"Temporary Sphinx config made by sphinx_run\"\"\"

extensions = ['sphinx_paw']"""


def get_source_dir():
    """Get source dir"""
    current_path = path.realpath(path.curdir)
    return path.join(current_path, 'docs')


def main():
    """Wrap sphinx-build"""

    source_dir = get_source_dir()

    config_path = path.join(source_dir, 'conf.py')
    restore_path = path.join(source_dir, 'conf.py.orig')
    if path.exists(config_path):
        rename(config_path, restore_path)

    with codecs.open(config_path, 'wb', 'utf-8') as config_fh:
        config_fh.write(conf_py_template)



