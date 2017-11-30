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

from avatarbuilder.AvatarSheet import AvatarSheet

import os
import xml.etree.ElementTree


class Avatar(object):
    def __init__(self, info):
        self._name = ''
        self._info = info
        self._sheet = None

    def name(self):
        return self._name

    def sheet(self):
        return self._sheet

    def deserialize(self, avatar, root_dir):
        from avatarbuilder.AvatarXml import AvatarXml

        # Get name
        self._name = avatar.get(AvatarXml.XML_ATTR_NAME)
        if not self._name:
            print('Error: Avatar is missing "{}" attribute'
                  .format(AvatarXml.XML_ATTR_NAME))
            return False

        # Deserialize sheet
        sheet_element = avatar.find(AvatarXml.XML_ELM_SHEET)
        if not sheet_element:
            print('Error: Avatar "{}" is missing <{}> tag'
                  .format(self._name, AvatarXml.XML_ELM_SHEET))
            return False

        self._sheet = AvatarSheet(root_dir)
        if not self._sheet.deserialize(sheet_element):
            return False

        return True

    def serialize(self, avatar_xml, relpath):
        from avatarbuilder.AvatarXml import AvatarXml

        # Serialize name
        avatar_xml.set(AvatarXml.XML_ATTR_NAME, self._name)

        # Serialize frames (TODO)
        relpath = os.path.join(relpath, '')  # Append trailing slash
        common = os.path.commonprefix([relpath, self._sheet.image()])
        image_path = self._sheet.image()[len(common):]
        # avatar_xml.set('image', image_path)

        # Serialize metadata
        info = self._info
        if info.author():
            author_tag = AvatarXml.XML_ELM_AUTHOR
            author = xml.etree.ElementTree.SubElement(avatar_xml, author_tag)
            author.text = info.author()

        if info.source():
            source_tag = AvatarXml.XML_ELM_SOURCE
            source = xml.etree.ElementTree.SubElement(avatar_xml, source_tag)
            source.text = info.source()

        if info.license():
            tag = AvatarXml.XML_ELM_LICENSE
            license_name = xml.etree.ElementTree.SubElement(avatar_xml, tag)
            license_name.text = info.license()

        if info.disclaimer():
            tag = AvatarXml.XML_ELM_DISCLAIMER
            disclaimer = xml.etree.ElementTree.SubElement(avatar_xml, tag)
            disclaimer.text = info.disclaimer()
