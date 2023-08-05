# -*- coding: utf-8 -*-
"""Internal exception classes"""


class ExtensionException(Exception):
    """Base class for all exctension exceptions"""


class RequireConfigSection(Exception):
    """Configuration section missed"""


class RequireConfigOption(Exception):
    """Configuration option missed"""


class RequireExtensionModule(Exception):
    """Extension module missed"""
