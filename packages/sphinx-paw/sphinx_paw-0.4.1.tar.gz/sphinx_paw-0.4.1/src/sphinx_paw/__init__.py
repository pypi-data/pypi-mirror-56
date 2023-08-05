# -*- coding: utf-8 -*-
from os import getenv
from os import path

from sphinx_paw.configurable import set_config_value
from sphinx_paw.constants import PACKAGE_NAME

__version__ = '0.4.1'

from datetime import datetime

from sphinx_paw.builders.confluence import init_confluence
from sphinx_paw.builders.latexpdf import init_latex
from sphinx_paw.configurable import ConfigFile
from sphinx_paw.constants import CONFIGURATION_SECTION_MAIN
from sphinx_paw.constants import CONFIGURATION_SECTION_METADATA
from sphinx_paw.extensions import Plugin
from sphinx_paw.main_params import init_main_params

from sphinx.util import logging

logger = logging.getLogger(__name__)


def setup(app):
    """Populate Sphinx configuration based on ini file"""
    logger.info(f"Prepare Sphinx configuration with {PACKAGE_NAME}")
    logger.debug(f"Load configuration from setup.cfg")
    config_file = ConfigFile(app, 'setup.cfg')

    metadata = config_file.get_section(CONFIGURATION_SECTION_METADATA)
    metadata.configure('project', 'Default project')
    metadata.configure('package', 'default')
    metadata.configure('author', 'Unknown author')
    metadata.configure('copyright', "{year}, {author}".format(
        year=datetime.now().year,
        author=metadata.author
    ))

    # Main language
    lang_type = getenv('LC_CTYPE', 'en_US.UTF8')
    if '.' in lang_type:
        language, encoding = lang_type.split('.')
    else:
        language = 'en_US'
    logger.info(f"Init language f{language}")
    set_config_value(app, 'language', language)

    # i18n
    logger.debug(f"Attach localization strings")
    locale_dir = path.join(path.abspath(path.dirname(__file__)), 'locales')
    app.add_message_catalog(PACKAGE_NAME, locale_dir)
    logger.info(f"Using locale path {locale_dir}")

    logger.debug("Configure main params")
    init_main_params(app, config_file)
    logger.info(f"{PACKAGE_NAME} ready")
