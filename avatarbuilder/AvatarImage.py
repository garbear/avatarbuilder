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

from avatarbuilder.AvatarAssets import AvatarAssets
from avatarbuilder.AvatarFrame import AvatarFrame
from avatarbuilder.AvatarSheet import Orientation

import collections
import cv2
import imageio
import numpy
import os
import subprocess


class AvatarImage(object):
    FRAME_PATH = '{0:02d}x'  # {0} - scaling factor

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
        sheet = avatar.sheet()

        # Generate path for avatar
        avatar_path = os.path.join(path, avatar.save_path())

        # Ensure path exists
        if not os.path.exists(avatar_path):
            os.makedirs(avatar_path)

        # Extract frames from image
        frames = AvatarImage._get_frames(image, sheet)
        if not frames:
            print('Error: Avatar "{}" - no frames extracted'
                  .format(avatar.name()))
            return False

        # Generate scaled frames
        for index in frames.keys():
            frame = frames[index]
            rgba_frame = frame[1]
            AvatarImage._generate_scaled_frames(avatar_path, rgba_frame, index)

        # Generate actions
        actions = AvatarImage._get_actions(avatar.actions(), frames)
        for action_tuple in actions:
            action = action_tuple[0]
            action_frames = action_tuple[1]
            AvatarImage._generate_action(avatar_path, action, action_frames)

        # Generate assets
        assets = avatar.assets()
        if assets is not None:
            assets_path = os.path.join(avatar_path, AvatarAssets.ASSETS_FOLDER)
            if not os.path.exists(assets_path):
                os.makedirs(assets_path)

            filename_index = 1
            for frame_index in assets.frames():
                if frame_index not in frames:
                    print('Error: Invalid asset frame index: {}'
                          .format(frame_index))
                    print('Valid indices are: {}'.format(frames.keys()))
                    return {}

                asset_frame = frames[frame_index][1]  # RGBA frame
                AvatarImage._generate_frame(assets_path, asset_frame,
                                            filename_index)
                filename_index += 1

        return True

    @staticmethod
    def _get_frames(image, sheet):
        frames = {}

        for row in range(sheet.rows()):
            for col in range(sheet.columns()):
                # Calculate frame index
                if sheet.orientation() == Orientation.HORIZONTAL:
                    index = row * sheet.columns() + col + 1
                else:
                    index = col * sheet.rows() + row + 1

                frame = AvatarImage._get_frame(image, sheet, row, col)

                if frame is not None:
                    rgb = numpy.zeros((frame.shape[0], frame.shape[1], 3),
                                      dtype=numpy.uint8)
                    rgba = numpy.zeros((frame.shape[0], frame.shape[1], 4),
                                       dtype=numpy.uint8)

                    if AvatarImage._subtract_background(frame, rgb, rgba):
                        frames[index] = (rgb, rgba)

        return frames

    @staticmethod
    def _get_frame(image, sheet, row, col):
        image_height, image_width = image.shape[:2]

        # Calculate the crop coordinates
        x = sheet.offsetx() + sheet.border() + \
            col * (sheet.width() + sheet.border())
        y = sheet.offsety() + sheet.border() + \
            row * (sheet.height() + sheet.border())
        w = sheet.width()
        h = sheet.height()

        # Verify we have a complete frame
        if y + h > image_height or x + w > image_width:
            print('Error: Row {}, col {} out of bounds for {}x{} image "{}"'
                  .format(row, col, image_width, image_height,
                          os.path.basename(sheet.image())))
            return None

        # Crop the image
        frame = AvatarImage._crop(image, x, y, w, h)

        return frame

    @staticmethod
    def _subtract_background(frame, rgb, rgba):
        # Detect the alpha value
        alpha = AvatarImage._get_alpha(frame)

        # Skip frame if empty
        if AvatarImage._is_empty(frame, alpha):
            return False

        # Set alpha color to transparent
        AvatarImage._set_transparent(frame, alpha, rgb, rgba)

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
    def _is_empty(frame, alpha):
        return not numpy.any(frame - alpha)

    @staticmethod
    def _set_transparent(frame, alpha, rgb, rgba):
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if numpy.array_equal(frame[i, j], alpha):
                    rgb[i, j] = numpy.array([0xFF, 0, 0xFF],
                                            dtype=numpy.uint8)  # Magenta
                    rgba[i, j] = numpy.array([0xFF, 0xFF, 0xFF, 0],
                                             dtype=numpy.uint8)  # Transparent white
                else:
                    if frame.shape[2] == 3:
                        rgb[i, j] = frame[i, j][::-1]
                        rgba[i, j] = [frame[i, j, 0],
                                      frame[i, j, 1],
                                      frame[i, j, 2],
                                      0xFF]
                    else:
                        rgb[i, j] = frame[i, j, :3][::-1]
                        rgba[i, j] = frame[i, j]

    @staticmethod
    def _get_actions(actions, frames):
        ret = []

        for action in actions:
            action_name = action.name()
            action_frames = []

            for frame_index in action.frames():
                if frame_index not in frames:
                    print('Error: Invalid action frame index: {}'
                          .format(frame_index))
                    print('Valid indices are: {}'.format(frames.keys()))
                    return {}

                frame = frames[frame_index]
                action_frames.append(frame)

            if action_frames:
                ret.append((action, action_frames))

        return ret

    @staticmethod
    def _generate_scaled_frames(path, frame, index):
        for scale in [1, 2, 4, 8, 16]:
            width, height = frame.shape[:2]

            # Don't scale past 512px
            if scale > 1 and (width * scale > 512 or height * scale > 512):
                break

            # Calculate output folder
            folder_name = AvatarImage.FRAME_PATH.format(scale)
            output_folder = os.path.join(path, folder_name)

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Scale frame
            if scale == 1:
                scaled = frame
            else:
                scaled = cv2.resize(frame, None, fx=scale, fy=scale,
                                    interpolation=cv2.INTER_NEAREST)

            # Generate frame
            AvatarImage._generate_frame(output_folder, scaled, index)

    @staticmethod
    def _generate_action(path, action, frames):
        # Calculate output path
        output_path = os.path.join(path, action.relpath())
        output_folder = os.path.dirname(output_path)

        # Ensure output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Generate frames
        frame_index = 1
        for frame in frames:
            rgba_frame = frame[1]
            AvatarImage._generate_frame(output_folder, rgba_frame, frame_index)
            frame_index += 1

        # Generate .gif
        rgb_frames = [frame[0] for frame in frames]
        AvatarImage._generate_gif(output_path, rgb_frames)

    @staticmethod
    def _generate_frame(output_folder, frame, index):
        # Calculate filename
        filename = AvatarFrame.FILE_NAME.format(index)
        frame_path = os.path.join(output_folder, filename)

        # Write image
        cv2.imwrite(frame_path, frame)

    @staticmethod
    def _generate_gif(gif_path, rgb_frames):
        durations = [1/6 for rgb_frame in rgb_frames]
        kwargs = {'duration': durations}
        imageio.mimwrite(gif_path, rgb_frames, None, **kwargs)

        # Compress gif and add transparency
        try:
            # TODO: Make magenta a parameter
            subprocess.call(['gifsicle', '-O3', '--transparent', '#FF00FF',
                             gif_path, '-o', gif_path])
        except FileNotFoundError:
            print('Error: gifsicle not found. See instructions in Readme.md')
