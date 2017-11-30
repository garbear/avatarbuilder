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
        if avatars.tag != 'avatars':
            print('Error: Expected root <avatars> tag, got <{}>'
                  .format(avatars.tag))
            return ret

        # Get common metadata
        info_element = avatars.find('info')
        if not info_element:
            print('Error: <info> tag not found')
            return ret

        info = AvatarInfo()
        if not info.deserialize(info_element):
            return ret

        # Scan for avatars
        for avatar_xml in avatars.findall('avatar'):
            avatar = Avatar(info)
            if avatar.deserialize(avatar_xml, root_dir):
                ret.append(avatar)

        return ret

    @staticmethod
    def save_avatars(avatars, avatars_xml_path):
        print('Saving {} avatars to {}'.format(len(avatars), avatars_xml_path))
        relpath = os.path.dirname(avatars_xml_path)
        avatars_xml = xml.etree.ElementTree.Element('avatars')
        for avatar in avatars:
            avatar_xml = xml.etree.ElementTree.SubElement(avatars_xml, 'avatar')
            AvatarXml.serialize_avatar(avatar, avatar_xml, relpath)

        dom = xml.dom.minidom.parseString(
            xml.etree.ElementTree.tostring(avatars_xml, encoding='UTF-8'))

        xmlstr = dom.toprettyxml(indent='\t')
        with open(avatars_xml_path, 'w') as file:
            file.write(xmlstr)

    @staticmethod
    def serialize_avatar(avatar, avatar_xml, relpath):
        avatar_xml.set('name', avatar.name())

        relpath = os.path.join(relpath, '')  # Append trailing slash
        common = os.path.commonprefix([relpath, avatar.image()])
        image_path = avatar.image()[len(common):]
        # avatar_xml.set('image', image_path)

        if avatar.author():
            author = xml.etree.ElementTree.SubElement(avatar_xml, 'author')
            author.text = avatar.author()

        if avatar.source():
            source = xml.etree.ElementTree.SubElement(avatar_xml, 'source')
            source.text = avatar.source()

        if avatar.license():
            license_name = xml.etree.ElementTree.SubElement(avatar_xml,
                                                            'license')
            license_name.text = avatar.license()

        if avatar.disclaimer():
            disclaimer = xml.etree.ElementTree.SubElement(avatar_xml,
                                                          'disclaimer')
            disclaimer.text = avatar.disclaimer()

        width = xml.etree.ElementTree.SubElement(avatar_xml, 'width')
        width.text = str(avatar.width())

        height = xml.etree.ElementTree.SubElement(avatar_xml, 'height')
        height.text = str(avatar.height())

        columns = xml.etree.ElementTree.SubElement(avatar_xml, 'columns')
        columns.text = str(avatar.columns())
        if avatar.offsetx() > 0:
            columns.set('offset', str(avatar.offsetx()))

        rows = xml.etree.ElementTree.SubElement(avatar_xml, 'rows')
        rows.text = str(avatar.rows())
        if avatar.offsety() > 0:
            rows.set('offset', str(avatar.offsety()))

        if avatar.border() > 0:
            border = xml.etree.ElementTree.SubElement(avatar_xml, 'border')
            border.text = str(avatar.border())
