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

    def deserialize(self, sheet, name):
        from avatarbuilder.AvatarXml import AvatarXml

        # Get image
        try:
            image = sheet.find(AvatarXml.XML_ELM_IMAGE).text
        except AttributeError:
            print('Error: Avatar "{}" sheet info is missing <{}> tag'
                  .format(name, AvatarXml.XML_ELM_IMAGE))
            return False

        if not image:
            print('Error: Avatar "{}" has empty <{}> tag'
                  .format(name, AvatarXml.XML_ELM_IMAGE))
            return False

        # Prepend root path
        self._image = os.path.join(self._root_dir, image)

        # Sanitize image path
        self._image = os.path.abspath(self._image)
        if not self._is_valid_path(self._root_dir, self._image):
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
            width = sheet.find(AvatarXml.XML_ELM_WIDTH).text
            self._width = int(width)
        except AttributeError:
            print('Error: Avatar "{}" sheet info is missing <{}> tag'
                  .format(name, AvatarXml.XML_ELM_WIDTH))
            return False
        except TypeError:
            print('Error: Avatar "{}" sheet info has invalid <{}> tag: "{}"'
                  .format(name, AvatarXml.XML_ELM_WIDTH, width))
            return False
        if self._width <= 0:
            print('Error: Avatar "{}" has invalid width: {}'
                  .format(name, width))
            return False

        # Get height
        try:
            height = sheet.find(AvatarXml.XML_ELM_HEIGHT).text
            self._height = int(height)
        except AttributeError:
            print('Error: Avatar "{}" sheet info is missing <{}> tag'
                  .format(name, AvatarXml.XML_ELM_HEIGHT))
            return False
        except TypeError:
            print('Error: Avatar "{}" sheet info has invalid <{}> tag: "{}"'
                  .format(name, AvatarXml.XML_ELM_HEIGHT, height))
            return False
        if self._height <= 0:
            print('Error: Avatar "{}" has invalid height: {}'
                  .format(name, height))
            return False

        # Get columns
        columns_element = sheet.find(AvatarXml.XML_ELM_COLUMNS)
        try:
            columns_text = columns_element.text
            self._columns = int(columns_text)
        except AttributeError:
            print('Error: Avatar "{}" sheet info is missing <{}> tag'
                  .format(name, AvatarXml.XML_ELM_COLUMNS))
            return False
        except TypeError:
            print('Error: Avatar "{}" sheet info has invalid <{}> tag: "{}"'
                  .format(name, AvatarXml.XML_ELM_COLUMNS, columns_text))
            return False

        # Get rows
        rows_element = sheet.find(AvatarXml.XML_ELM_ROWS)
        try:
            rows_text = rows_element.text
            self._rows = int(rows_text)
        except AttributeError:
            print('Error: Avatar "{}" sheet info  is missing <{}> tag'
                  .format(name, AvatarXml.XML_ELM_ROWS))
            return False
        except TypeError:
            print('Error: Avatar "{}" sheet info has invalid <{}> tag: "{}"'
                  .format(name, AvatarXml.XML_ELM_ROWS, rows_text))
            return False

        # Get offsetx
        offsetx_text = columns_element.get(AvatarXml.XML_ATTR_OFFSET)
        if offsetx_text:
            try:
                self._offsetx = int(offsetx_text)
            except TypeError:
                print('Error: Avatar "{}" has invalid column offset: "{}"'
                      .format(name, offsetx_text))
                return False

        # Get offsety
        offsety_text = rows_element.get(AvatarXml.XML_ATTR_OFFSET)
        if offsety_text:
            try:
                self._offsety = int(offsety_text)
            except TypeError:
                print('Error: Avatar "{}" has invalid row offset: "{}"'
                      .format(name, offsety_text))
                return False

        # Get border
        try:
            border = sheet.find(AvatarXml.XML_ELM_BORDER).text
            self._border = int(border)
        except AttributeError:
            pass
        except TypeError:
            print('Error: Avatar "{}" has invalid <{}> tag: "{}"'
                  .format(name, AvatarXml.XML_ELM_BORDER, border))
            return False

        # Get orientation
        try:
            orientation = sheet.find(AvatarXml.XML_ELM_ORIENTATION).text
            if orientation not in [
                Orientation.HORIZONTAL.value,
                Orientation.VERTICAL.value
            ]:
                print('Error: Invalid orientation: {}'
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
