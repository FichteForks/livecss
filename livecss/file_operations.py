# -*- coding: utf-8 -*-

"""
    livecss.file_operations
    ~~~~~~~~~

    This module implements file operation functions.

"""

# std lib
from os import listdir
from os import remove as rm
from os.path import exists, basename, join
from glob import glob
from .theme import theme

import sublime

from .helpers import compact, flatten


def clean_junk():
    """Cleans `Color Scheme - Default` directory"""
    packages_path = sublime.packages_path()
    old_themes = [glob(join(packages_path, f, theme.prefix + '*')) for f in listdir(packages_path)]
    for path in compact(flatten(old_themes)):
        rm_if_exists(path)


def rm_if_exists(path):
    """Removes path if it exists"""
    if exists(path):
        rm(path)


def rm_theme(path):
    """Removes given `path` and .cache file for it;
    if it is a generateted theme file"""
    if basename(path).startswith(theme.prefix):
        rm_if_exists(path)
        rm_if_exists(path + '.cache')
