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
    @staticmethod
    def deserialize(frame_elm):
        from avatarbuilder.AvatarXml import AvatarXml

        frame = -1

        try:
            frame = int(frame_elm.text)
        except ValueError:
            print('Error: <{}> tag is not an integer: "{}"'
                  .format(AvatarXml.XML_ELM_FRAME, frame_elm.text))

        return frame
