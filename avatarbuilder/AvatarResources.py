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

import os
import shutil


class AvatarResources(object):
    _RESOURCES_DIR = 'resources'

    @staticmethod
    def copy_files(source, target):
        files = [
            'resources/icon.png',
            'CC-BY-SA-3.0-LICENSE.txt',
            'Readme.md'
        ]

        print('Copying {} static files'.format(len(files)))

        # Ensure resources directory exists
        resources_path = os.path.join(target, AvatarResources._RESOURCES_DIR)
        if not os.path.exists(resources_path):
            os.makedirs(resources_path)

        # Copy files
        for file in files:
            shutil.copy(os.path.join(source, file), os.path.join(target, file))
