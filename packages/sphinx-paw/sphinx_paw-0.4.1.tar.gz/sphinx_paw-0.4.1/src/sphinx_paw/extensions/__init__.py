# -*- coding: utf-8 -*-
"""Init package as Sphinx plugin"""
import glob
import importlib
import sys
import types
from abc import abstractmethod
from os import path

from sphinx.application import Sphinx
from sphinx.util import logging

from sphinx_paw import ConfigFile
from sphinx_paw.constants import NOTSET
from sphinx_paw.constants import OPTION_PLUGIN_DIR
from sphinx_paw.constants import OPTION_PLUGIN_DIR_DEFAULT
from sphinx_paw.constants import SECTION_PLUGINS_NAME
from sphinx_paw.templates import Template

logger = logging.getLogger(__name__)


class Plugin(object):
    """Documentation builder plugin"""

    def __init__(self, app, config):
        assert isinstance(app, Sphinx)
        assert isinstance(config, ConfigFile)
        self.app = app
        self.config = config

        self.debug = logger.debug
        self.info = logger.info
        self.warning = logger.warning
        self.error = logger.error
        self.critical = logger.critical

        self.info(f"{self.__class__.__name__} ready")

    def __call__(self):
        logger.info(f"Run {self.__class__.__name__}")
        self.run()

    @abstractmethod
    def run(self):
        """Run plugin before builders"""
        pass

    @classmethod
    def get_plugins_dir(cls, app, config):
        """Get plugins dir"""
        assert isinstance(app, Sphinx)
        assert isinstance(config, ConfigFile)
        plugins_config = config.get_section(SECTION_PLUGINS_NAME)
        return plugins_config.get(OPTION_PLUGIN_DIR, OPTION_PLUGIN_DIR_DEFAULT)

    @classmethod
    def get_plugins(cls, app, config):
        """Get available plugins"""
        logger.info("Loading plugins")
        plugins_dir = path.join(app.srcdir, Plugin.get_plugins_dir(app, config))

        logger.info(f"Process all plugins in {plugins_dir}")
        if not path.exists(plugins_dir):
            logger.info(f"No plugins found")
            return ()
        plugins_pattern = path.join(plugins_dir, '*.py')

        def plugin_modules():
            """Load plugin modules"""
            logger.info("Loading plugin modules")
            for module_path in glob.glob(plugins_pattern):
                module_name = path.basename(module_path)[:-3]
                logger.info(f"Loading module {module_name}")

                sys.path.insert(0, plugins_dir)
                m = importlib.import_module(module_name)
                sys.path.pop(0)

                assert isinstance(m, types.ModuleType)
                logger.info(f"Load plugin file {m.__name__}")
                yield m

        def plugin_classes():
            """Generate plugin instances"""
            for m in plugin_modules():
                names = (x for x in m.__dict__)
                items = (m.__getattribute__(x) for x in names)
                classes = (x for x in items if type(x) == type)
                plugins = (
                    x for x in classes
                    if issubclass(x, Plugin) and x is not Plugin
                )

                for plugin_class in plugins:
                    logger.info(f"Load plugin class {plugin_class.__name__}")
                    yield plugin_class

        # generate instances
        return (x(app, config) for x in plugin_classes())

    @classmethod
    def run_all_found(cls, app, config):
        """Run all found plugins"""
        logger.info("Run plugins")
        for plugin in cls.get_plugins(app, config):
            plugin()

    def template(self, template_name, allow_default=False):
        """Load template by filename"""
        if Template.template_engine is NOTSET:
            Template.configure(self.app, self.config)
        return Template(template_name, allow_default=allow_default)
