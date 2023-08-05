# -*- coding: utf-8 -*-
"""Get configuration information from setup.cfg"""

from os import path

from six.moves.configparser import ConfigParser
from sphinx.application import Sphinx

from sphinx_paw.constants import IGNORE_CHANGES
from sphinx_paw.constants import NOTSET
from sphinx_paw.constants import REBUILD_ON_CHANGE
from sphinx_paw.exceptions import RequireConfigOption
from sphinx_paw.exceptions import RequireConfigSection

conf = ConfigParser()


def set_config_value(app, option, value, rebuild=REBUILD_ON_CHANGE):
    """Add configuration value or reset if already present"""
    assert isinstance(app, Sphinx)

    assert rebuild in [REBUILD_ON_CHANGE, IGNORE_CHANGES]
    if option in app.config:
        app.config[option] = value
    else:
        app.add_config_value(option, value, rebuild)


class NoSuchSection(Exception):
    """Wrap NoSectionError"""
    pass


class ConfigFileSection(object):
    """Wrap configuration file section"""

    def __init__(self, config_file, name):
        assert isinstance(config_file, ConfigFile)
        self._name = name
        self._config_file = config_file

    def get(self, key, default):
        """Get value of key or default if key not present"""
        return self._config_file.get(self._name, key, default)

    def __getattr__(self, item):
        """Get configuration value as attribute"""
        return self.get(item, default=NOTSET)

    @property
    def app(self):
        """Return Sphinx instance as application"""
        return self._config_file.sphinx

    def configure(self, name, default, option=None, rebuild=REBUILD_ON_CHANGE):
        """Populate section option value as Sphinx config option

        :param name: option name in ini section
        :param default: default value
        :param option: option name in sphinx config
        :param rebuild: rebuild on option change
        """
        option = option or name
        option_value = self.get(name, default)
        set_config_value(self.app, option, option_value, rebuild)


class ConfigFile(object):
    """Wrapper to get additional options from ini file"""

    def __init__(self, app, file_path):
        assert path.exists(file_path), "No such file %s" % file_path
        assert isinstance(app, Sphinx)

        self.sphinx = app
        self._file_path = file_path
        self._config = ConfigParser()
        super(ConfigFile, self).__init__()
        self._config.read([self._file_path])

    def get(self, section, key, default=NOTSET):
        """Get value of key in section, default if key not present"""
        from six.moves.configparser import NoSectionError
        from six.moves.configparser import NoOptionError

        try:
            return self._config.get(section, key)
        except NoSectionError:
            if default != NOTSET:
                return default
            raise RequireConfigSection(
                "Section %s is not defined and no default value for %s" % (
                    section, key
                )
            )

        except NoOptionError:
            if default != NOTSET:
                return default
            raise RequireConfigOption(
                "Missed required option [%s]%s, default not set" % (
                    section, key
                )
            )

    def assert_has_section(self, section_name):
        """Ensure config has section"""
        if not self._config.has_section(section_name):
            raise RequireConfigSection(
                "Required configuration section {section_name}".format(
                    section_name=section_name
                )
            )

    def has_section(self, section_name):
        """Check if config has section"""
        return self._config.has_section(section_name)

    def __getattr__(self, item):
        """Get section using attribute-style access"""
        if not self._config.has_section(item):
            raise NoSuchSection("No section [%s]" % item)
        return ConfigFileSection(self, item)

    def __getitem__(self, item):
        """Get section using dict-style access"""
        return self.__getattr__(item)

    def get_section(self, section_name, init_if_missed=True):
        """Get section using method-style access"""
        if not self.has_section(section_name) and init_if_missed:
            self._config.add_section(section_name)
        return self[section_name]
