# -*- coding: utf-8 -*-
"""Provide setup.py integration"""
from sphinx.setup_command import BuildDoc

from sphinx_paw.sphinx_wrapper import get_source_dir


class Build(BuildDoc):
    """Wrap distutils build doc command"""

    def __init__(self, dist):
        super(Build, self).__init__(dist)

        self.fresh_env = False
        self.all_files = False
        self.pdb = False
        self.source_dir = None
        self.build_dir = None
        self.builder = None
        self.warning_is_error = False
        self.project = ''
        self.version = ''
        self.release = ''
        self.today = ''
        self.config_dir = None
        self.link_index = False
        self.copyright = ''
        self.verbosity = 0
        self.traceback = False
        self.nitpicky = False

    def finalize_options(self):
        """Init internal options"""
        self.source_dir = get_source_dir()
        self.announce('Using source directory %s' % self.source_dir)

        super(Build, self).initialize_options()


