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

from avatarbuilder.AvatarSheet import Orientation

import collections
import cv2
import imageio
import numpy
import os


class AvatarImage(object):
    FRAME_PATH = '{0:02d}x'  # {0} - scaling factor
    FILE_NAME = '{0:03d}.png'  # {0} - frame index
    ASSETS_FOLDER = 'assets'
    ACTION_ANIMATION = '{0}.gif'  # {0} - action name

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

        # Extract frames from image
        frames = AvatarImage._get_frames(image, sheet)
        if not frames:
            print('Error: Avatar "{}" - no frames extracted'
                  .format(avatar.name()))
            return False

        # Generate scaled frames
        for index in frames.keys():
            frame = frames[index]
            AvatarImage._generate_scaled_frames(path, frame, index)

        # Generate actions
        actions = AvatarImage._get_actions(avatar.actions(), frames)
        for action_name in actions.keys():
            action_frames = actions[action_name]
            AvatarImage._generate_action(path, action_name, action_frames)

        # Generate assets
        assets = avatar.assets()
        if assets is not None:
            filename_index = 1
            for frame_index in assets.frames():
                if frame_index not in frames:
                    print('Error: Invalid asset frame index: {}'
                          .format(frame_index))
                    print('Valid indices are: {}'.format(frames.keys()))
                    return {}

                asset_frame = frames[frame_index]
                AvatarImage._generate_asset(path, asset_frame, filename_index)
                filename_index += 1

        return True

    @staticmethod
    def _get_frames(image, sheet):
        frames = {}

        for j in range(sheet.rows()):
            for i in range(sheet.columns()):
                # Calculate frame index
                if sheet.orientation() == Orientation.HORIZONTAL:
                    index = j * sheet.rows() + i + 1
                else:
                    index = i * sheet.columns() + j + 1

                frame = AvatarImage._get_frame(image, sheet, i, j)

                if frame is not None:
                    frame = AvatarImage._subtract_background(frame)

                    if frame is not None:
                        frames[index] = frame

        return frames

    @staticmethod
    def _get_frame(image, sheet, row, col):
        image_width, image_height = image.shape[:2]

        # Calculate the crop coordinates
        x = sheet.offsetx() + sheet.border() + \
            row * (sheet.width() + sheet.border())
        y = sheet.offsety() + sheet.border() + \
            col * (sheet.height() + sheet.border())
        w = sheet.width()
        h = sheet.height()

        # Verify we have a complete frame
        if y + h >= image_height or x + w >= image_width:
            return None

        # Crop the image
        frame = AvatarImage._crop(image, x, y, w, h)

        return frame

    @staticmethod
    def _subtract_background(frame):
        # Detect the alpha value
        alpha = AvatarImage._get_alpha(frame)

        # Skip frame if empty
        if AvatarImage._is_empty(frame, alpha):
            return None

        # Set alpha color to transparent
        frame = AvatarImage._set_transparent(frame, alpha)

        return frame

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
    def _set_transparent(frame, alpha):
        new_frame = numpy.zeros((frame.shape[0], frame.shape[1], 4),
                                dtype=numpy.uint8)
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

    @staticmethod
    def _get_actions(actions, frames):
        ret = {}

        for action in actions:
            action_name = action.name()
            action_frames = []

            for frame_index in action.frames():
                if frame_index not in frames:
                    print('Error: Invalid action frame index: {}'.format(frame_index))
                    print('Valid indices are: {}'.format(frames.keys()))
                    return {}

                frame = frames[frame_index]
                action_frames.append(frame)

            if action_frames:
                ret[action_name] = action_frames

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

            # Scale frame
            if scale == 1:
                scaled = frame
            else:
                scaled = cv2.resize(frame, None, fx=scale, fy=scale,
                                    interpolation=cv2.INTER_NEAREST)

            # Generate frame
            AvatarImage._generate_frame(output_folder, frame, index)

    @staticmethod
    def _generate_action(path, action_name, frames):
        # Calculate output folder
        output_folder = os.path.join(path, action_name)

        # Ensure output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Generate frames
        frame_index = 1
        for frame in frames:
            AvatarImage._generate_frame(output_folder, frame, frame_index)
            frame_index += 1

        # Generate .gif
        AvatarImage._generate_gif(output_folder, frames, action_name)

    @staticmethod
    def _generate_asset(path, frame, index):
        # Calculate output folder
        output_folder = os.path.join(path, AvatarImage.ASSETS_FOLDER)

        # Generate frame
        AvatarImage._generate_frame(output_folder, frame, index)

    @staticmethod
    def _generate_frame(output_folder, frame, index):
        # Calculate filename
        filename = AvatarImage.FILE_NAME.format(index)
        frame_path = os.path.join(output_folder, filename)

        # Write image
        cv2.imwrite(frame_path, frame)

    @staticmethod
    def _generate_gif(output_folder, frames, action_name):
        # Calculate filename
        filename = AvatarImage.ACTION_ANIMATION.format(action_name)
        gif_path = os.path.join(output_folder, filename)

        # Remove alpha channel
        images = [AvatarImage._remove_alpha(frame) for frame in frames]
        # Write image

        print('Generating "{}"'.format(gif_path))  # TODO
        durations = [1/12 for image in images]
        kwargs = {'duration': durations}
        imageio.mimwrite(gif_path, images, None, **kwargs)

    @staticmethod
    def _remove_alpha(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
