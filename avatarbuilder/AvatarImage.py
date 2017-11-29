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
    FRAME_PATH = 'frames-{}x'  # {} - scaling factor

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
        image_width, image_height = image.shape[:2]

        index = 1
        alpha = None
        for j in range(avatar.rows()):
            for i in range(avatar.columns()):
                # Calculate the crop coordinates
                x = avatar.offsetx() + avatar.border() + \
                    i * (avatar.width() + avatar.border())
                y = avatar.offsety() + avatar.border() + \
                    j * (avatar.height() + avatar.border())
                w = avatar.width()
                h = avatar.height()

                # Verify we have a complete frame
                if y + h >= image_height or x + w >= image_width:
                    continue

                # Crop the image
                frame = AvatarImage._crop(image, x, y, w, h)

                # Detect the alpha value
                if alpha is None:
                    alpha = AvatarImage._get_alpha(frame)

                # TODO: Skip frame if empty
                # empty = not numpy.any(frame - alpha)

                frame = AvatarImage._set_transparent(frame, alpha)

                for scale in [1, 2, 4, 8, 16]:
                    width = w * scale
                    height = h * scale

                    if scale > 1 and (height > 512 or width > 512):
                        break

                    # Scale frame
                    if scale == 1:
                        scaled = frame
                    else:
                        scaled = cv2.resize(frame, None, fx=scale, fy=scale,
                                            interpolation=cv2.INTER_NEAREST)

                    # Calculate output folder
                    folder_name = AvatarImage.FRAME_PATH.format(scale)
                    output_folder = os.path.join(path, folder_name)

                    # Ensure output folder exists
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)

                    # Calculate filename
                    filename = '{}.png'.format(index)
                    frame_path = os.path.join(output_folder, filename)
                    index += 1

                    # Write image
                    cv2.imwrite(frame_path, scaled)

        return True

    @staticmethod
    def _crop(frame, x, y, w, h):
        return frame[y: y + h, x: x + w, :]

    @staticmethod
    def _get_alpha(frame):
        top_left = frame[0, 0]
        top_right = frame[0, frame.shape[1] - 1]
        bottom_left = frame[frame.shape[0] - 1, frame.shape[1] - 1]
        bottom_right = frame[frame.shape[0] - 1, 0]

        corners = [top_left, top_right, bottom_left, bottom_right]

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

    @staticmethod
    def _set_transparent(frame, alpha):
        new_frame = numpy.zeros((frame.shape[0], frame.shape[1], 4))
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if any(frame[i][j] - alpha):
                    if frame.shape[2] == 4:
                        new_frame[i][j] = frame[i][j]
                    else:
                        new_frame[i][j] = [frame[i][j][0],
                                           frame[i][j][1],
                                           frame[i][j][2],
                                           255]

        return new_frame
