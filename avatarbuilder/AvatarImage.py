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

                # TODO: If frame is empty, continue

                frame_path = os.path.join(output_path, '{}.png'.format(index))
                index = index + 1
                cv2.imwrite(frame_path, frame)

        return True
