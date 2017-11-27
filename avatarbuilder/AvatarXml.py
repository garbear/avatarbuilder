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

from avatarbuilder.Avatar import Avatar

import os
import xml.etree.ElementTree


class AvatarXml(object):
    FILE_NAME = 'avatars.xml'

    @staticmethod
    def load_avatars(avatars_xml_path):
        avatars = []

        try:
            tree = xml.etree.ElementTree.parse(avatars_xml_path)
        except FileNotFoundError:
            print('Error: File not found: {}'.format(avatars_xml_path))
        except xml.etree.ElementTree.ParseError as e:
            print('Error: Failed to parse XML: {}'.format(e))
        else:
            root = tree.getroot()
            avatars = AvatarXml._deserialize_avatars(root, avatars_xml_path)

        return avatars

    @staticmethod
    def _deserialize_avatars(avatars, avatars_xml_path):
        root_dir = os.path.dirname(avatars_xml_path)

        # Resolve root directory to protect against malicious path traversal
        root_dir = os.path.abspath(root_dir)

        ret = []

        if avatars.tag != 'avatars':
            print('Error: Expected root <avatars> tag, got <{}>'
                  .format(avatars.tag))
        else:
            # Get common metadata
            author = ''
            source = ''
            license_name = ''
            disclaimer = ''
            for child in avatars:
                if child.tag == 'author':
                    author = child.text
                elif child.tag == 'source':
                    source = child.text
                elif child.tag == 'license':
                    license_name = child.text
                elif child.tag == 'disclaimer':
                    disclaimer = child.text

            # Scan for avatars
            for avatar_xml in avatars.findall('avatar'):
                avatar = Avatar(author=author,
                                source=source,
                                license_name=license_name,
                                disclaimer=disclaimer)
                if avatar.deserialize(avatar_xml, root_dir):
                    ret.append(avatar)

        return ret
