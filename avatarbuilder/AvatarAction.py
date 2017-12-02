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

from avatarbuilder.AvatarFrame import AvatarFrame

import os
import xml.etree.ElementTree


class AvatarAction(object):
    ACTION_ANIMATION = '{0}.gif'  # {0} - action name

    def __init__(self, avatar):
        self._avatar = avatar
        self._name = ''
        self._frames = []

    def name(self):
        return self._name

    def frames(self):
        return self._frames

    def relpath(self):
        action_folder = self._name

        filename = AvatarAction.ACTION_ANIMATION.format(self._name)
        relpath = os.path.join(action_folder, filename)

        return relpath

    def deserialize(self, action):
        from avatarbuilder.AvatarXml import AvatarXml

        # Get name
        self._name = action.get(AvatarXml.XML_ATTR_NAME)
        if not self._name:
            print('Error: Avatar "{}" - <{}> tag is missing "{}" attribute'
                  .format(self._avatar.name(), AvatarXml.XML_ELM_ACTION,
                          AvatarXml.XML_ATTR_NAME))
            return False

        # Get frames
        for frame_elm in action.findall(AvatarXml.XML_ELM_FRAME):
            frame = AvatarFrame.deserialize(frame_elm, self._avatar.name())
            if frame > 0:
                self._frames.append(frame)

        if not self._frames:
            print('Error: Avatar "{}" - <{}> tag contains no valid frames'
                  .format(self._avatar.name(), AvatarXml.XML_ELM_ACTION))
            return False

        return True

    def serialize(self, actions_elm, avatars_folder):
        from avatarbuilder.AvatarXml import AvatarXml

        action_tag = AvatarXml.XML_ELM_ACTION
        action_elm = xml.etree.ElementTree.SubElement(actions_elm, action_tag)
        action_elm.set(AvatarXml.XML_ATTR_NAME, self._name)

        avatar_dir = os.path.join(avatars_folder, self._avatar.save_path())
        action_path = os.path.join(avatar_dir, self.relpath())
        action_elm.text = action_path
