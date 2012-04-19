# -*- coding: utf-8 -*-
"""
    livecss.helpers
    ~~~~~~~~~

    This module implements some python helper objects.
    > import re
    > one_of_os = one_of(['win', 'mac', 'linux'])
    > bool(re.match(one_of_os, 'win'))
    True

"""


def one_of(seq):
    "Return regex which matches one element of seq"
    seq = [r'\b%s\b' % el for el in seq]
    return reduce(lambda x, y: str(x) + '|' + str(y), seq)

escape = lambda s: "\'" + s + "\'"

compact = lambda seq: [el for el in seq if el]
flatten = lambda seq: [item for sublist in seq for item in sublist]
