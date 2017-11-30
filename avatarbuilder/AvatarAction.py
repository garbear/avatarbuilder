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


class AvatarAction(object):
    def __init__(self):
        self._name = ''
        self._frames = []

    def name(self):
        return self._name

    def frames(self):
        return self._frames

    def deserialize(self, action):
        from avatarbuilder.AvatarXml import AvatarXml

        # Get name
        self._name = action.get(AvatarXml.XML_ATTR_NAME)
        if not self._name:
            print('Error: <{}> tag is missing "{}" attribute'
                  .format(AvatarXml.XML_ELM_ACTION, AvatarXml.XML_ATTR_NAME))
            return False

        # Get frames
        for frame_elm in action.findall(AvatarXml.XML_ELM_FRAME):
            frame = AvatarFrame.deserialize(frame_elm)
            if frame > 0:
                self._frames.append(frame)

        if not self._frames:
            print('Error: <{}> tag contains no valid frames'
                  .format(AvatarXml.XML_ELM_ACTION))
            return False

        return True
