# -*- coding: utf-8 -*-

"""
    livecss.settings
    ~~~~~~~~~

    This module implements a wrapper for ST settings (local and global).

"""
from sublime import load_settings, View, save_settings

# from .wrappers import PerFileConfig, Settings


class Settings(object):
    """ Wrapper around sublime settings,
    uses ST settings to store instance properties.

    """
    _settings_file = ''
    in_memory = True

    def __init__(self, settings_file, in_memory=True):
        """
        @param {str|sublime.View} settings_file: settings file name OR instance of sublime.View
        @param {bool} in_memory: save on each attribute setting

        """
        self._in_memory = in_memory
        self._settings_file = settings_file

        if settings_file.__class__ == View:
            self._settings = settings_file.settings()
        else:
            self._settings = load_settings(settings_file)

    def __getattribute__(self, attr):
        if not attr.startswith("_"):
            return self._settings.get(attr)

        return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        object.__setattr__(self, attr, value)
        if not attr.startswith("_"):
            self._settings.set(attr, value)
            if not self._in_memory:
                self._save()

    def __contains__(self, attr):
        if not getattr(self, attr) == None:
            return True

    def __getitem__(self, attr):
        return getattr(self, attr)

    def __setitem__(self, attr, value):
        setattr(self, attr, value)

    def _save(self):
        save_settings(self._settings_file)


# dict to hold already loaded settings wrappers
settings = dict()


def settings_for(view):
    # TODO: re-rework this, should not be hard
    """Wrapper function to load global and/or local Settings references"""
    bid = "global"

    if view.__class__ == View:
        bid = view.buffer_id()

    if bid in settings:
        return settings[bid]

    class wrapper:
        pass

    if view.__class__ == View:
        wrapper.local = Settings(view)
    wrapper.glob = Settings('livecss-settings.sublime-settings', False)

    settings[bid] = wrapper
    return wrapper
