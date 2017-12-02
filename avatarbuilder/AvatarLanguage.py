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

import os


class AvatarLanguage(object):
    LANGUAGE_PATH = 'resources/language/English/strings.po'

    ADDON_STRING_ID_START = 30000

    def __init__(self, avatars):
        self._strings = {}
        self._next_string_id = AvatarLanguage.ADDON_STRING_ID_START

        for avatar in avatars:
            self._strings[avatar.name()] = self._next_string_id
            self._next_string_id += 1

    def get_string_id(self, s):
        return self._strings.get(s, -1)

    def generate_language(self, resources_dir):
        language_path = os.path.join(resources_dir,
                                     AvatarLanguage.LANGUAGE_PATH)

        print('Appending language file "{}"'.format(language_path))

        with open(language_path, 'a') as file:
            for line in self._strings.keys():
                string_id = self.get_string_id(line)
                if string_id >= 0:
                    content = self.get_message_block(string_id, line)
                    file.write(content)

    @staticmethod
    def get_message_block(string_id, line):
        content = '\n'
        content += 'msgctxt "#{}"\n'.format(string_id)
        content += 'msgid "{}"\n'.format(line)
        content += 'msgstr ""\n'
        return content
