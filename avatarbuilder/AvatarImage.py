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

import collections
import cv2
import numpy
import os


class AvatarImage(object):
    FRAME_PATH = 'frames'

    @staticmethod
    def load_image(image_path):
        image = None

        with open(image_path, 'rb') as img_stream:
            buf = img_stream.read()
            data = numpy.asarray(bytearray(buf), dtype=numpy.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

        return image

    @staticmethod
    def generate_frames(image, avatar, path):
        # Ensure output path exists
        output_path = os.path.join(path, AvatarImage.FRAME_PATH)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        index = 1
        for j in range(avatar.rows()):
            for i in range(avatar.columns()):
                x = avatar.offsetx() + avatar.border() + \
                    i * (avatar.width() + avatar.border())
                y = avatar.offsety() + avatar.border() + \
                    j * (avatar.height() + avatar.border())
                w = avatar.width() - avatar.border()
                h = avatar.height() - avatar.border()

                frame = image[y: y + h, x: x + w, :]

                top_left = frame[0, 0]
                top_right = frame[0, frame.shape[1] - 1]
                bottom_left = frame[frame.shape[0] - 1, frame.shape[1] - 1]
                bottom_right = frame[frame.shape[0] - 1, 0]

                corners = [top_left, top_right, bottom_left, bottom_right]
                alpha = AvatarImage._get_alpha(corners)

                # Check if frame is empty
                empty = not numpy.any(frame - alpha)
                filename = '{}{}.png'.format(index, '-empty' if empty else '')

                frame_path = os.path.join(output_path, filename)
                index += 1
                cv2.imwrite(frame_path, frame)

        return True

    @staticmethod
    def _get_alpha(corners):
        corner_strings = [corner.tostring() for corner in corners]

        corner_dict = {
            corner_strings[0]: corners[0],
            corner_strings[1]: corners[1],
            corner_strings[2]: corners[2],
            corner_strings[3]: corners[3]
        }

        data = collections.Counter(corner_strings)
        mode = data.most_common(1)[0][0]
        return corner_dict[mode]
