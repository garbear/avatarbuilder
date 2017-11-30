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

import enum
import os


class Orientation(str, enum.Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class AvatarSheet(object):
    def __init__(self, root_dir):
        self._root_dir = root_dir
        self._image = ''
        self._width = 0
        self._height = 0
        self._columns = 0
        self._rows = 0
        self._offsetx = 0
        self._offsety = 0
        self._border = 0
        self._orientation = Orientation.HORIZONTAL

    def image(self):
        return self._image

    def width(self):
        return self._width

    def height(self):
        return self._height

    def columns(self):
        return self._columns

    def rows(self):
        return self._rows

    def offsetx(self):
        return self._offsetx

    def offsety(self):
        return self._offsety

    def border(self):
        return self._border

    def orientation(self):
        return self._orientation

    def deserialize(self, sheet):
        # Get image
        try:
            image = sheet.find('image').text
        except AttributeError:
            print('Error: Avatar "{}" is missing <image> tag'
                  .format(self._name))
            return False

        # Prepend root path
        self._image = os.path.join(self._root_dir, image)

        # Sanitize image path
        self._image = os.path.abspath(self._image)
        if not self._is_valid_path(self._root_dir, self._image):
            from avatarbuilder.AvatarXml import AvatarXml
            print()
            print('------------------------------------------------------------'
                  '--------------------')
            print('WARNING: FILE TRIED TO ESCAPE DIRECTORY!!!')
            print('File: {}'.format(AvatarXml.FILE_NAME))
            print('Directory: "{}"'.format(self._root_dir))
            print('Image path: "{}"'.format(self._image))
            print('------------------------------------------------------------'
                  '--------------------')
            print()
            raise Exception('UNSAFE FILE: avatars.xml - SEE LOG!!!')

        # Get width
        try:
            width = sheet.find('width').text
            self._width = int(width)
        except AttributeError:
            print('Error: Avatar "{}" is missing <width> tag'
                  .format(self._name))
            return False
        except ValueError:
            print('Error: Avatar "{}" has invalid <width> tag: "{}"'
                  .format(self._name, width))
            return False

        # Get height
        try:
            height = sheet.find('height').text
            self._height = int(height)
        except AttributeError:
            print('Error: Avatar {} is missing <height> tag'
                  .format(self._name))
            return False
        except ValueError:
            print('Error: Avatar "{}" has invalid <height> tag: "{}"'
                  .format(self._name, height))
            return False

        # Get columns
        columns_element = sheet.find('columns')
        try:
            columns_text = columns_element.text
            self._columns = int(columns_text)
        except AttributeError:
            print('Error: Avatar {} is missing <columns> tag'
                  .format(self._name))
            return False
        except ValueError:
            print('Error: Avatar "{}" has invalid <columns> tag: "{}"'
                  .format(self._name, columns_text))
            return False

        # Get rows
        rows_element = sheet.find('rows')
        try:
            rows_text = rows_element.text
            self._rows = int(rows_text)
        except AttributeError:
            print('Error: Avatar {} is missing <rows> tag'
                  .format(self._name))
            return False
        except ValueError:
            print('Error: Avatar "{}" has invalid <rows> tag: "{}"'
                  .format(self._name, rows_text))
            return False

        # Get offsetx
        offsetx_text = columns_element.get('offset')
        if offsetx_text:
            try:
                self._offsetx = int(offsetx_text)
            except ValueError:
                print('Error: Avatar "{}" has invalid column offset: "{}"'
                      .format(self._name, offsetx_text))
                return False

        # Get offsety
        offsety_text = rows_element.get('offset')
        if offsety_text:
            try:
                self._offsety = int(offsety_text)
            except ValueError:
                print('Error: Avatar "{}" has invalid row offset: "{}"'
                      .format(self._name, offsety_text))
                return False

        # Get border
        try:
            border = sheet.find('border').text
            self._border = int(border)
        except AttributeError:
            pass
        except ValueError:
            print('Error: Avatar "{}" has invalid <border> tag: "{}"'
                  .format(self._name, border))
            return False

        # Get orientation
        try:
            orientation = sheet.find('orientation').text
            if orientation not in [
                Orientation.HORIZONTAL.value,
                Orientation.VERTICAL.value
            ]:
                print('Error: invalid orientation: {}'
                      .format(orientation))
                return False
            self._orientation = orientation
        except AttributeError:
            pass

        return True

    @staticmethod
    def _is_valid_path(root_dir, image):
        common_prefix = os.path.commonprefix([root_dir, image])
        return common_prefix == root_dir
