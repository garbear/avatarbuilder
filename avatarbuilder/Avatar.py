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

from avatarbuilder.AvatarAction import AvatarAction
from avatarbuilder.AvatarAssets import AvatarAssets
from avatarbuilder.AvatarSheet import AvatarSheet

import os
import xml.etree.ElementTree


class Avatar(object):
    def __init__(self, info):
        self._name = ''
        self._info = info
        self._sheet = None
        self._actions = []
        self._assets = None

    def name(self):
        return self._name

    def info(self):
        return self._info

    def sheet(self):
        return self._sheet

    def actions(self):
        return self._actions

    def assets(self):
        return self._assets

    def save_path(self):
        # Replace spaces with underscores for pngcrush
        avatar_path = self._name.replace(' ', '_')

        return avatar_path

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
        if not self._sheet.deserialize(sheet_element, self._name):
            return False

        # Deserialize actions
        actions_elm = avatar.find(AvatarXml.XML_ELM_ACTIONS)
        if actions_elm:
            for action_elm in actions_elm.findall(AvatarXml.XML_ELM_ACTION):
                action = AvatarAction(self)
                if not action.deserialize(action_elm):
                    return False
                self._actions.append(action)
        else:
            # TODO: Allow frame generation without actions
            print('Error: Avatar "{}" has no actions defined'
                  .format(self._name))
            return False

        # Deserialize assets
        assets_elm = avatar.find(AvatarXml.XML_ELM_ASSETS)
        if assets_elm:
            assets = AvatarAssets()
            if assets.deserialize(assets_elm, self._name):
                self._assets = assets

        return True

    def serialize(self, avatar_xml, language):
        from avatarbuilder.AvatarXml import AvatarXml

        # Translate name to string ID
        name_id = language.get_string_id(self._name)
        if name_id < 0:
            print('Error: invalid ID {} for string "{}"'
                  .format(name_id, self._name))
            return False

        # Serialize name
        avatar_xml.set(AvatarXml.XML_ATTR_NAME, self._name)
        avatar_xml.set(AvatarXml.XML_ATTR_NAME_ID, str(name_id))

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

        # Serialize actions
        if self._actions:
            tag = AvatarXml.XML_ELM_ACTIONS
            actions_elm = xml.etree.ElementTree.SubElement(avatar_xml, tag)
            for action in self._actions:
                action.serialize(actions_elm)

        return True
