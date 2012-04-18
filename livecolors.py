# -*- coding: utf-8 -*-

"""
    livecolors
    ~~~~~~~~~

    ST commands.

"""

import sublime_plugin

# local imports
from livecss.colorizer import colorize_file, uncolorize_file
from livecss.file_operations import clean_junk
from livecss.state import state_for
from livecss.theme import theme, is_colorized
from livecss.utils import (need_colorization, generate_default_settings,
                           generate_menu, colorize_on_select_new_theme)
from livecss.settings import settings_for


class EventManager(sublime_plugin.EventListener):
    def __init__(self):
        # before anything
        clean_junk()
        # TODO: provide this in repo and use defaults when not found
        generate_default_settings()

    def on_load(self, view):
        # set hook to recolorize if different theme was chosen
        theme.on_select_new_theme(lambda: colorize_on_select_new_theme(view))
        if need_colorization(view):
            colorize_file(view, state_for(view))

    def on_close(self, view):
        state = state_for(view)
        if is_colorized(state.theme_path):
            uncolorize_file(view, state)

    # TODO: this is not triggered when "replacing" content
    # TODO: DOES NOT WORK AS EXPECTED!!
    def on_modified(self, view):
        state = state_for(view)
        if need_colorization(view):
            colorize_file(view, state)
        elif is_colorized():
            uncolorize_file(view, state)

    def on_activated(self, view):
        generate_menu(view)

        state = state_for(view)
        if state and state.theme_path:
            # set file's own theme path, because we use one per file
            theme.set(state.theme_path)
        state.focused = True

        # TODO: this is not really needed (from testing), uncomment otherwise
        # if need_colorization(view):
        #     colorize_file(view, state, True)


class CssColorizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        colorize_file(self.view, state_for(self.view), True)


class CssUncolorizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        uncolorize_file(self.view, state_for(self.view))


class ToggleLocalLiveCssCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        state = state_for(view)
        s = settings_for(view)

        # retrieve default local state from global setting
        if s.local.autocolorize is None:
            s.local.autocolorize = s.glob.autocolorize or False

        s.local.autocolorize = not s.local.autocolorize

        if s.local.autocolorize:
            colorize_file(view, state, True)
        else:
            uncolorize_file(view, state)

        generate_menu(view)


class ToggleGlobalLiveCssCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        state = state_for(view)
        s = settings_for(view)

        s.glob.autocolorize = not s.glob.autocolorize

        if need_colorization(view):
            colorize_file(view, state, True)
        elif is_colorized():
            uncolorize_file(view, state)

        generate_menu(view)
