# -*- coding: utf-8 -*-
"""Define internal constants to runtime and setup"""

PACKAGE_NAME = __package__

CONFIGURATION_EXTENDED = 'documentation_builders'

CONFIGURATION_SECTION_PREFIX = 'build'

CONFIGURATION_SECTION_METADATA = 'metadata'

CONFIGURATION_SECTION_MAIN = 'sphinx'

NOTSET = object()

DEFAULT_SECTION_PREFIX = 'build'
DEFAULT_SECTION_SUFFIX = ''


OPTION_BUILDER_PREFIX = 'builder_prefix'
OPTION_BUILDER_SUFFIX = 'builder_suffix'

REBUILD_ON_CHANGE = True
IGNORE_CHANGES = False

BUILDER_HTML_SECTION = 'html'

SECTION_PLUGINS_NAME = 'plugins'
OPTION_PLUGIN_DIR = 'plugin'
OPTION_PLUGIN_DIR_DEFAULT = '_plugins'

SECTION_TEMPLATES_NAME = 'templates'
OPTION_TEMPLATES_DIR = 'templates'
OPTION_TEMPLATES_DIR_DEFAULT = '_templates'
