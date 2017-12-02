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


class AvatarFrame(object):
    FILE_NAME = '{0:03d}.png'  # {0} - frame index

    @staticmethod
    def deserialize(frame_elm, avatar_name):
        from avatarbuilder.AvatarXml import AvatarXml

        frame = -1

        try:
            frame = int(frame_elm.text)
        except TypeError:
            print('Error: Avatar "{}" - <{}> tag is not an integer: "{}"'
                  .format(avatar_name, AvatarXml.XML_ELM_FRAME, frame_elm.text))

        return frame
