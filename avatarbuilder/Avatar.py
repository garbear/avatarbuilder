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


class Avatar(object):
    def __init__(self, info):
        self._name = ''
        self._info = info
        self._image = ''
        self._width = 0
        self._height = 0
        self._columns = 0
        self._rows = 0
        self._offsetx = 0
        self._offsety = 0
        self._border = 0
        self._orientation = Orientation.HORIZONTAL

    def name(self):
        return self._name

    def author(self):
        return self._info.author()

    def source(self):
        return self._info.source()

    def license(self):
        return self._info.license()

    def disclaimer(self):
        return self._info.disclaimer()

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

    def deserialize(self, avatar, root_dir):
        # Get name
        self._name = avatar.get('name')
        if not self._name:
            print('Error: Avatar is missing "name" attribute')
            return False

        # Get image
        self._image = avatar.get('image')
        if not self._image:
            print('Error: Avatar "{}" is missing "image" attribute'
                  .format(self._name))
            return False

        # Prepend root path
        self._image = os.path.join(root_dir, self._image)

        # Sanitize image path
        self._image = os.path.abspath(self._image)
        if os.path.commonprefix([self._image, root_dir]) != root_dir:
            from avatarbuilder.AvatarXml import AvatarXml
            print()
            print('------------------------------------------------------------'
                  '--------------------')
            print('WARNING: FILE TRIED TO ESCAPE DIRECTORY!!!')
            print('File: {}'.format(AvatarXml.FILE_NAME))
            print('Directory: "{}"'.format(root_dir))
            print('Image path: "{}"'.format(self._image))
            print('------------------------------------------------------------'
                  '--------------------')
            print()
            raise Exception('UNSAFE FILE: avatars.xml - SEE LOG!!!')

        # Get dimensions
        try:
            width = avatar.find('width').text
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
            height = avatar.find('height').text
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
        columns_element = avatar.find('columns')
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
        rows_element = avatar.find('rows')
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
            border = avatar.find('border').text
            self._border = int(border)
        except AttributeError:
            pass
        except ValueError:
            print('Error: Avatar "{}" has invalid <border> tag: "{}"'
                  .format(self._name, border))
            return False

        # Get orientation
        try:
            orientation = avatar.find('orientation').text
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
