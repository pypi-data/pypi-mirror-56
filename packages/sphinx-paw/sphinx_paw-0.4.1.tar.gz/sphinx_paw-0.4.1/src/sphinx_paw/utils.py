# -*- coding: utf-8 -*-
"""Internal utility functions"""
from sphinx_paw.configurable import ConfigFile
from sphinx_paw.constants import CONFIGURATION_EXTENDED
from sphinx_paw.constants import CONFIGURATION_SECTION_MAIN
from sphinx_paw.constants import DEFAULT_SECTION_PREFIX
from sphinx_paw.constants import DEFAULT_SECTION_SUFFIX
from sphinx_paw.constants import NOTSET
from sphinx_paw.constants import OPTION_BUILDER_PREFIX
from sphinx_paw.constants import OPTION_BUILDER_SUFFIX


def get_main_sphinx_section_name():
    """Build main sphinx config section name"""
    return '%s_%s' % (DEFAULT_SECTION_PREFIX, CONFIGURATION_SECTION_MAIN)


def get_private_section_name(config, name, prefix=NOTSET, suffix=NOTSET):
    """Make sphinx builder section name using prefix, name and suffix"""
    assert isinstance(config, ConfigFile)

    if prefix is NOTSET:
        prefix = DEFAULT_SECTION_PREFIX
    prefix = config.get(CONFIGURATION_EXTENDED, OPTION_BUILDER_PREFIX, prefix)

    if prefix:
        prefix += '_'

    if suffix is NOTSET:
        suffix = DEFAULT_SECTION_SUFFIX

    suffix = config.get(CONFIGURATION_EXTENDED, OPTION_BUILDER_SUFFIX, suffix)

    if suffix:
        name += '_'

    return '%s%s%s' % (prefix, name, suffix)
