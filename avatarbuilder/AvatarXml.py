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
from avatarbuilder.AvatarInfo import AvatarInfo

import os
import xml.dom.minidom
import xml.etree.ElementTree


class AvatarXml(object):
    FILE_NAME = 'avatars.xml'

    XML_ELM_ROOT = 'avatars'
    XML_ELM_INFO = 'info'
    XML_ELM_AUTHOR = 'author'
    XML_ELM_SOURCE = 'source'
    XML_ELM_LICENSE = 'license'
    XML_ELM_DISCLAIMER = 'disclaimer'
    XML_ELM_AVATAR = 'avatar'
    XML_ELM_SHEET = 'sheet'
    XML_ELM_IMAGE = 'image'
    XML_ELM_WIDTH = 'width'
    XML_ELM_HEIGHT = 'height'
    XML_ELM_COLUMNS = 'columns'
    XML_ELM_ROWS = 'rows'
    XML_ELM_BORDER = 'border'
    XML_ELM_ORIENTATION = 'orientation'
    XML_ELM_ACTIONS = 'actions'
    XML_ELM_ACTION = 'action'
    XML_ELM_FRAME = 'frame'
    XML_ELM_ASSETS = 'assets'

    XML_ATTR_NAME = 'name'
    XML_ATTR_NAME_ID = 'nameid'
    XML_ATTR_OFFSET = 'offset'

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

        # Check root tag
        if avatars.tag != AvatarXml.XML_ELM_ROOT:
            print('Error: Expected root <{}> tag, got <{}>'
                  .format(AvatarXml.XML_ELM_ROOT, avatars.tag))
            return ret

        # Get common metadata
        info_element = avatars.find(AvatarXml.XML_ELM_INFO)
        if not info_element:
            print('Error: {} - <{}> tag not found'
                  .format(AvatarXml.FILE_NAME, AvatarXml.XML_ELM_INFO))
            return ret

        info = AvatarInfo()
        if not info.deserialize(info_element):
            return ret

        # Scan for avatars
        for avatar_xml in avatars.findall(AvatarXml.XML_ELM_AVATAR):
            avatar = Avatar(info)
            if avatar.deserialize(avatar_xml, root_dir):
                ret.append(avatar)

        return ret

    @staticmethod
    def save_avatars(avatars, language, avatars_xml_path):
        print('Saving {} avatars to {}'.format(len(avatars), avatars_xml_path))

        relpath = os.path.dirname(avatars_xml_path)
        avatars_xml = xml.etree.ElementTree.Element(AvatarXml.XML_ELM_ROOT)
        for avatar in avatars:
            tag = AvatarXml.XML_ELM_AVATAR
            avatar_xml = xml.etree.ElementTree.SubElement(avatars_xml, tag)
            avatar.serialize(avatar_xml, language, relpath)

        dom = xml.dom.minidom.parseString(
            xml.etree.ElementTree.tostring(avatars_xml, encoding='UTF-8'))

        xmlstr = dom.toprettyxml(indent='\t')
        with open(avatars_xml_path, 'w') as file:
            file.write(xmlstr)
