#
# Copyright (C) 2017 Garrett Brown
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.
#


class AvatarInfo(object):
    def __init__(self):
        self._author = ''
        self._source = ''
        self._license = ''
        self._disclaimer = ''

    def author(self):
        return self._author

    def source(self):
        return self._source

    def license(self):
        return self._license

    def disclaimer(self):
        return self._disclaimer

    def deserialize(self, info):
        try:
            self._author = info.find('author').text
        except AttributeError:
            print('Error: avatars.xml is missing <author> tag')
            return False

        try:
            self._source = info.find('source').text
        except AttributeError:
            print('Error: avatars.xml is missing <source> tag')
            return False

        try:
            self._license = info.find('license').text
        except AttributeError:
            print('Error: avatars.xml is missing <license> tag')
            return False

        try:
            self._disclaimer = info.find('disclaimer').text
        except AttributeError:
            pass

        return True
