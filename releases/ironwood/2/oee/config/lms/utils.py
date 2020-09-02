# -*- coding: utf-8 -*-

import yaml
import os

from django.core.exceptions import ImproperlyConfigured


class Configuration(dict):
    """
    Try getting a setting from the settings.yml or secrets.yml files placed in
    the directory passed when initializing the configuration instance.
    """

    def __init__(self, dir=None, *args, **kwargs):
        """
        Initialize with the path to the directory in which the configuration is
        to be found.
        """
        super(Configuration, self).__init__(*args, **kwargs)

        if dir is None:
            self.settings = {}

        else:
            # Load the content of a `settings.yml` file placed in the current
            # directory if any. This file is where customizable settings are stored
            # for a given environment.
            try:
                with open(os.path.join(dir, "settings.yml")) as f:
                    settings = yaml.load(f.read()) or {}
            except IOError:
                settings = {}

            # Load the content of a `secrets.yml` file placed in the current
            # directory if any. This file is where sensitive credentials are stored
            # for a given environment.
            try:
                with open(os.path.join(dir, "secrets.yml")) as f:
                    credentials = yaml.load(f.read()) or {}
            except IOError:
                credentials = {}

            settings.update(credentials)
            self.settings = settings

    def __call__(self, var_name, formatter=str, *args, **kwargs):
        """
        The config returns in order of priority:

            - the value set in the secrets.yml file,
            - the value set in the settings.yml file,
            - the value set as environment variable
            - the value passed as default.

        If the value is passed as a string, a type is forced via the function passed in
        the "formatter" kwarg.

        Raise an "ImproperlyConfigured" error if the name is not found, except
        if the `default` key is given in kwargs (using kwargs allows to pass a
        default to None, which is different from not passing any default):

            $ config = Configuration('path/to/config/directory')
            $ config('foo')  # raise ImproperlyConfigured error if `foo` is not defined
            $ config('foo', default='bar')  # return 'bar' if `foo` is not defined
            $ config('foo', default=None)  # return `None` if `foo` is not defined
        """
        try:
            value = self.settings[var_name]
        except KeyError:
            try:
                value = formatter(os.environ[var_name])
            except KeyError:
                if "default" in kwargs:
                    value = kwargs["default"]
                else:
                    raise ImproperlyConfigured(
                        'Please set the "{:s}" variable in a settings.yml file, a secrets.yml '
                        "file or an environment variable.".format(var_name)
                    )
        # If a formatter is specified, force the value but only if it was passed as a string
        if isinstance(value, basestring):
            value = formatter(value.encode("utf-8"))

        return value

    def get(self, name, *args, **kwargs):
        """
        edX is loading the content of 2 json files to settings.ENV_TOKEN and settings.AUTH_TOKEN
        They have started calling these attributes anywhere in the code base, so we must make
        sure that the following call works (and the same for AUTH_TOKEN):

            settings.ENV_TOKEN.get('ANY_SETTING_NAME')

        That's what this method will do after we add this to our settings:
           ```
           config = Configuration('path/to/my/settings/directory.yml')
           ENV_TOKEN = config
           AUTH_TOKEN = config
           ```
        """
        try:
            default = args[0]
        except IndexError:
            # As a first approach, all defaults that are not provided by Open edX are set to None.
            # If this creates a problem, we can either:
            #    - make sure we provide a value for this setting in our yaml files,
            #    - make a PR to Open edX to provide a better default for this setting.
            default = None
        return self(name, default=default)
