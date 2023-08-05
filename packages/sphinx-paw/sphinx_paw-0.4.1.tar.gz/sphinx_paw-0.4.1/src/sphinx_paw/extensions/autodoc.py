# -*- coding: utf-8 -*-

"""Configure HTML builder's options"""

from sphinx.application import Sphinx

from sphinx_paw.configurable import ConfigFile
from sphinx_paw.configurable import set_config_value
from sphinx_paw.constants import BUILDER_HTML_SECTION
from sphinx_paw.utils import get_private_section_name


def init_autodoc(app, config):
    """Configure autodoc options"""
    assert isinstance(app, Sphinx)
    assert isinstance(config, ConfigFile)

    private_section_name = get_private_section_name(
        config,
        BUILDER_HTML_SECTION
    )
    if not config.has_section(private_section_name):
        return

    autodoc_default_options = {
        'member-order': 'bysource',
        'private-members': False,
        'undoc-members': False,
        'exclude-members': '__weakref__ __builtins__ __loader__',
    }

    # define theme to use as html template
    set_config_value(app, 'autodoc_default_options', autodoc_default_options)

