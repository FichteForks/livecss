# -*- coding: utf-8 -*-

"""
    livecss.colorizer
    ~~~~~~~~~

    This module implements some useful utilities.

"""
import os

import sublime

# local imports

from .state import state_for
from .theme import theme, uncolorized_path
from .colorizer import colorize_file
from .menu import create_menu
from .settings import settings_for


def colorize_on_select_new_theme(view):
    state = state_for(view)
    if not state.theme_path:
        return
    if uncolorized_path(state.theme_path) != uncolorized_path(theme.abspath):
        # here is small hack to colorize after we change the theme
        # TODO: find out better solution
        sublime.set_timeout(lambda: colorize_file(view, state, True), 200)


def generate_menu(view):
    # TODO: improve this
    s = settings_for(view)
    lstate = s.local.autocolorize
    if s.local.autocolorize == 'undefined':
        if s.glob.autocolorize:
            lstate = True
        else:
            lstate = False
    create_menu(lstate, s.glob.autocolorize)


def is_colorizable(view):
    s = settings_for(view)
    point = view.sel()[0].begin()
    file_scope = view.scope_name(point).split()[0]
    file_name = view.file_name()
    if file_name:
        file_ext = file_name.split('.')[-1]
    else:
        file_ext = ""
    if file_scope in s.glob.colorized_formats or file_ext in s.glob.colorized_formats:
        return True


def need_colorization(view):
    s = settings_for(view)
    # TODO: This setup needs a command to discard local settings
    if not (s.local.autocolorize is None):
        return s.local.autocolorize
    return s.glob.autocolorize and is_colorizable(view)


def generate_default_settings():
    if not os.path.exists(os.path.join(sublime.packages_path(), 'User', 'livecss-settings.sublime-settings')):
        s = settings_for(False)
        s.glob.colorized_formats = ["source.css", "source.css.less", "source.sass"]
        s.glob.autocolorize = True
