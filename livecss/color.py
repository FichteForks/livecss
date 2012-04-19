# -*- coding: utf-8 -*-

"""
    livecss.color
    ~~~~~~~~~

    This module implements some useful utilities.

"""

import colorsys

from .colors import named_colors


def to_ints(seq):
    return [int(num) for num in seq]


def to_floats(seq):
    return [float(num) for num in seq]

numberdict = {'i': 'int',
              'f': 'float'}


def to_numbers(seq, types):
    ret = list()
    for i in seq.keys():
        op = False
        if types[i] in numberdict:
            op = numberdict[types[i]]
        elif types[i] in numberdict.values():
            op = types[i]
        if op:
            ret.append(eval(op + '(' + seq[i] + ')'))


class Color(object):
    """Convenience to work with colors"""

    def __init__(self, color):
        self.color = color

    @property
    def hex(self):
        color = self.color
        if color in named_colors:
            hex_color = named_colors[color]
        elif color.startswith('rgb'):
            if color.startswith('rgba'):
                r, g, b, a = color.strip('rgba()').split(',')
            else:
                r, g, b = color.strip('rgb()').split(',')
            hex_color = self._rgb_to_hex((r, g, b))

        elif color.startswith('hsl'):
            if color.startswith('hsla'):
                h, s, l, a = to_floats(color.strip('hsla()').replace('%', '').split(','))
            else:
                h, s, l = to_floats(color.strip('hsl()').replace('%', '').split(','))

            h, s, l = (h / 360.0, s / 100.0, l / 100.0)
            hex_color = self._rgb_to_hex([255 * i for i in colorsys.hls_to_rgb(h, l, s)])

        else:
            if len(color) == 4:
                # 3 sign hex
                color = '#' + color[1] * 2 + color[2] * 2 + color[3] * 2
            if color.startswith('0x'):
                # 0x123456
                color = '#' + color[2:]

            hex_color = color

        return hex_color

    @property
    def undash(self):
        return self.hex.lstrip('#')

    @property
    def opposite(self):
        r, g, b = self._hex_to_rgb(self.undash)
        brightness = (r + b + g) / 3
        if brightness > 130:
            return '#000000'
        else:
            return '#ffffff'

    def __repr__(self):
        return self.hex

    def __str__(self):
        return self.hex

    def __eq__(self, other):
        return self.hex == other

    def __hash__(self):
        return hash(self.hex)

    def _rgb_to_hex(self, rgb):
        if len(rgb) == 4:
            #rgba
            rgb = rgb[0:3]

        if not isinstance(rgb[0], int):
            if str(rgb[0]).endswith('%'):
                # percentage notation
                r = int(rgb[0].rstrip('%')) * 255 / 100
                g = int(rgb[1].rstrip('%')) * 255 / 100
                b = int(rgb[2].rstrip('%')) * 255 / 100
                return self._rgb_to_hex((r, g, b))

            rgb = to_ints(rgb)

        return '#%02x%02x%02x' % tuple(x for x in rgb)

    def _hex_to_rgb(self, hex):
        return tuple(int(hex[i:i + 2], 16) for i in range(0, 6, 2))
