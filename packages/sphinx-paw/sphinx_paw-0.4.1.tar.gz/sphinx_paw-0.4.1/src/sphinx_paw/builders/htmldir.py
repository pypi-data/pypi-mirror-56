# -*- coding: utf-8 -*-
"""Configure HTML builder's options"""

from sphinx.application import Sphinx

from sphinx_paw.configurable import ConfigFile
from sphinx_paw.configurable import set_config_value
from sphinx_paw.constants import BUILDER_HTML_SECTION
from sphinx_paw.utils import get_private_section_name


def init_html(app, config):
    """Configure HTML and HTML Help builder options"""
    assert isinstance(app, Sphinx)
    assert isinstance(config, ConfigFile)

    private_section_name = get_private_section_name(
        config,
        BUILDER_HTML_SECTION
    )
    if not config.has_section(private_section_name):
        return

    # define theme to use as html template
    set_config_value(app, 'html_theme', 'sphinx_rtd_theme')
    # setup path for additional static files to use in html output
    set_config_value(app, 'html_static_path', ['_static'])
    # add
    set_config_value(app, 'html_context', {'css_files': ['_static/tables.css']})

    # Custom sidebar templates, must be a dictionary that maps document names
    # to template names.
    #
    # This is required for the alabaster theme
    # refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
    html_sidebars = {
        '**': [
            'relations.html',
            # needs 'show_related': True theme option to display
            'searchbox.html',
        ]
    }
    set_config_value(app, 'html_sidebars', html_sidebars)

    html_baseurl = '/'
    set_config_value(app, 'html_baseurl', html_baseurl)

    html_copy_source = False
    set_config_value(app, 'html_copy_source', html_copy_source)

    html_show_sourcelink = False
    set_config_value(app, 'html_show_sourcelink', html_show_sourcelink)

    html_link_suffix = '.html'
    set_config_value(app, 'html_link_suffix', html_link_suffix)

    html_show_sphinx = False
    set_config_value(app, 'html_show_sphinx', html_show_sphinx)

    html_search_language = 'ru'
    set_config_value(app, 'html_search_language', html_search_language)

    html_show_copyright = False
    set_config_value(app, 'html_show_copyright', html_show_copyright)
