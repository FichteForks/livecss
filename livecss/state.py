"""
    livecss.state
    ~~~~~~~~~

    This module implements state object and function to associate state with view

"""

from .theme import is_colorized
from os.path import exists


class State(object):
    def __init__(self, view):
        self.count = 0
        self.theme_path = ""
        self.saved_colors = []
        self.saved_regions = []
        self.view = view

    @property
    def is_dirty(self):
        """Indicates if state was changed"""

        highlighted_regions = get_highlighted_regions(self.view, self.count)

        # check if regions have changed
        if highlighted_regions == self.regions or (not self.regions and not highlighted_regions):
            is_dirty = False
        else:
            is_dirty = True

        # check if lengths of regions changed
        if not is_dirty:
            for reg_pair in zip(self.saved_regions, self.regions):
                if abs(reg_pair[0].a - reg_pair[0].b) != abs(reg_pair[1].a - reg_pair[1].b):
                    is_dirty = True

        # save current regions
        self.saved_regions = self.regions
        return is_dirty

    @property
    def need_generate_theme_file(self):
        """Indicates if new color definition appeared in current file"""

        # check if there are new colors in view
        if not self.saved_colors or set(self.colors) - set(self.saved_colors):
            need_generate = True
        else:
            need_generate = False

        # save current colors
        self.saved_colors = self.colors
        # check if theme_path is "valid"
        return need_generate or not is_colorized(self.theme_path) or not exists(self.theme_path)


def get_highlighted_regions(view, last_highlighted_region):
    """Return currently highlighted regions for this file."""

    if not last_highlighted_region:
        return
    regions = []
    for i in range(last_highlighted_region):
        region = view.get_regions('css_color_%d' % i)
        if region:
            regions.append(region[0])
    return regions


# dict to hold states
states = dict()


class state_for(object):
    """Store and retrieve state"""
    def __init__(self, view):
        """Create or retrieve state for given view
        self.focused = unique attribute for all states
        """
        if view.buffer_id() not in states:
            states[view.buffer_id()] = State(view)
        self.view = view

    def __getattribute__(self, attr):
        if attr == 'focused':
            bid, is_focused = states['focused']
            if bid == self.view.buffer_id():
                return True
        elif attr == 'view' or attr.startswith('__'):
            return object.__getattribute__(self, attr)

        return getattr(states[self.view.buffer_id()], attr)

    def __setattr__(self, attr, value):
        object.__setattr__(self, attr, value)
        if attr == 'focused':
            states['focused'] = [self.view.buffer_id(), value]
        elif attr != 'view' and not attr.startswith('__'):
            setattr(states[self.view.buffer_id()], attr, value)
