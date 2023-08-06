#!/usr/bin/env python3
"""
    Copyright (C) ilias iliadis, 2019-11-24; ilias iliadis <iliadis@kekbay.gr>

    This file is part of «gettextcodecs library».

    «gettextcodecs library» is free software:
    you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    «gettextcodecs library» is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with «gettextcodecs library».
    If not, see <http://www.gnu.org/licenses/>.
"""

import os
import codecs
import encodings

def get_text_codecs(as_list = False):
    """ Get a dict of all known codec names for text processing.

    The dictionary is constructed using the default name of encoding
    and contains a list with all aliases, if any.

    Parameters:

    - as_list: Boolean. Optional. Return a single list.
    Defaults to False.
    """
    encoding_files = os.listdir(os.path.dirname(encodings.__file__))
    the_codecs = {}
    for anitem in encoding_files:
        if anitem.endswith(".py") and (anitem != "__init__.py"):
            try:
                acodec = codecs.lookup(anitem[:-3])
                if acodec._is_text_encoding:
                    #append the known name
                    the_codecs[acodec.name] = [k for k, v \
                            in encodings.aliases.aliases.items() \
                            if acodec.name == v]
            except LookupError:
                pass
    if as_list:
        thelist = [k for k in the_codecs]
        for anitem in thelist[:]:
            if len(the_codecs[anitem]):
                thelist += ([k for k in the_codecs[anitem]])
        return thelist
    return the_codecs

if __name__ == '__main__':
    print(get_text_codecs())
