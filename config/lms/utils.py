# -*- coding: utf-8 -*-

import yaml
import os

from django.core.exceptions import ImproperlyConfigured


class Configuration(dict):
    """
    Try getting a setting from the settings.yml or secrets.yml files placed in
    the directory passed when initializing the configuration instance.
    """

    def __init__(self, dir, *args, **kwargs):
        """
        Initialize with the path to the directory in which the configuration is
        to be found.
        """
        super(Configuration, self).__init__(*args, **kwargs)

        # Load the content of a `settings.yml` file placed in the current
        # directory if any. This file is where customizable settings are stored
        # for a given environment.
        try:
            with open(os.path.join(dir, "settings.yml")) as f:
                settings = yaml.load(f.read())
        except IOError:
            settings = {}
        else:
            settings = settings or {}

        # Load the content of a `secrets.yml` file placed in the current
        # directory if any. This file is where sensitive credentials are stored
        # for a given environment.
        try:
            with open(os.path.join(dir, "credentials.vault.yml")) as f:
                credentials = yaml.load(f.read())
        except IOError:
            credentials = {}
        else:
            credentials = credentials or {}

        settings.update(credentials)
        self.settings = settings

    def __call__(self, var_name, *args, **kwargs):
        """
        The config returns in order of priority:

            - the value set in the secrets.yml file,
            - the value set in the settings.yml file,
            - the value passed as default.

        Raise an "ImproperlyConfigured" error if the name is not found, except
        if the `default` key is given in kwargs (using kwargs allows to pass a
        default to None, which is different from not passing any default):

            $ config = Configuration('path/to/config/directory')
            $ config('foo')  # raise ImproperlyConfigured error if `foo` is not defined
            $ config('foo', default='bar')  # return 'bar' if `foo` is not defined
            $ config('foo', default=None)  # return `None` if `foo` is not defined
        """
        try:
            return self.settings[var_name]
        except KeyError:
            if "default" in kwargs:
                return kwargs["default"]
            raise ImproperlyConfigured(
                'Please set the "{:s}" variable in a `settings.yml` '
                "or  secrets.yml` file.".format(var_name)
            )
