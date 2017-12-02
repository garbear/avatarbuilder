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


class AvatarAssets(object):
    ASSETS_FOLDER = 'assets'

    def __init__(self):
        self._frames = []

    def frames(self):
        return self._frames

    def deserialize(self, action, avatar_name):
        from avatarbuilder.AvatarXml import AvatarXml

        # Get frames
        for frame_elm in action.findall(AvatarXml.XML_ELM_FRAME):
            frame = AvatarFrame.deserialize(frame_elm, avatar_name)
            if frame > 0:
                self._frames.append(frame)

        if not self._frames:
            print('Error: Avatar "{}" - <{}> tag contains no valid frames'
                  .format(avatar_name, AvatarXml.XML_ELM_ASSETS))
            return False

        return True
