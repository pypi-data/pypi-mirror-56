# -*- coding: utf-8 -*-
from os import path

from jinja2 import Environment
from sphinx.application import Sphinx
from jinja2 import Template as JinjaTemplate

from sphinx_paw import ConfigFile
from sphinx_paw.constants import NOTSET
from sphinx_paw.constants import OPTION_TEMPLATES_DIR
from sphinx_paw.constants import OPTION_TEMPLATES_DIR_DEFAULT
from sphinx_paw.constants import SECTION_TEMPLATES_NAME
from sphinx_paw.rewritable import rewritable_file_path
from sphinx_paw.translation import translator

TEMPLATES_DEFAULT_PATH = path.realpath(path.dirname(__file__))


class TemplateEngine(object):
    """Jinja page template engine"""

    def __init__(self, app, config):
        assert isinstance(app, Sphinx)
        assert isinstance(config, ConfigFile)
        self.app = app
        self.config = config

        self.templates_config = config.get_section(SECTION_TEMPLATES_NAME)

        env = Environment(extensions=['jinja2.ext.i18n'])
        env.install_gettext_translations(translator)

    def get_templates_path(self):
        """Return templates path"""
        return path.join(self.app.srcdir, self.templates_config.get(
            OPTION_TEMPLATES_DIR, OPTION_TEMPLATES_DIR_DEFAULT
        ))

    def get_template_file_path(self, filename, allow_default=True):
        """Get filepath for filename"""
        templates_path = self.get_templates_path()
        default_path = allow_default and TEMPLATES_DEFAULT_PATH or None
        return rewritable_file_path(
            self.app, filename,
            local_path=path.realpath(templates_path),
            default_path=default_path
        )

    def get_template_content(self, filename, allow_default=True):
        """Get template"""
        file_path = self.get_template_file_path(
            filename, allow_default=allow_default
        )
        with open(file_path, 'rb') as content_fh:
            content = content_fh.read().decode()
            return content


class Template(object):
    """Jinja page template"""
    template_engine = NOTSET

    @classmethod
    def configure(cls, app, config):
        """Configure class template engine"""
        assert isinstance(app, Sphinx)
        assert isinstance(config, ConfigFile)
        if cls.template_engine is NOTSET:
            cls.template_engine = TemplateEngine(app, config)

    def __init__(self, filename, allow_default=True, raise_if_not_found=True):
        if self.__class__.template_engine is NOTSET:
            raise NotImplementedError(
                f"call {self.__class__}.configure(app, config) first"
            )
        super().__init__()
        self.filename = filename
        self.allow_default = allow_default

        self.filepath = self.template_engine.get_template_file_path(
            filename,
            allow_default=allow_default
        )
        self.file_exists = path.exists(self.filepath)
        if not self.file_exists and raise_if_not_found:
            raise FileNotFoundError(
                f"No such template {self.filepath}. "
                f"Either create it or init with raise_if_not_found=False"
            )

    def get_content(self):
        """Get template content"""
        if not self.file_exists:
            raise FileNotFoundError(f"No such template {self.filepath}.")
        return self.template_engine.get_template_content(
            self.filename,
            allow_default=self.allow_default
        )

    def render(self, **context):
        """Render template into string"""
        template = JinjaTemplate(self.get_content())
        return template.render(**context)

    def render_into(self, target_path, **context):
        """Render template into file"""
        with open(target_path, 'w') as target_fh:
            target_fh.write(self.render(**context))






