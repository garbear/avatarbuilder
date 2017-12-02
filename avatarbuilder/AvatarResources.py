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

from avatarbuilder.AvatarLanguage import AvatarLanguage

import os
import shutil


class AvatarResources(object):
    @staticmethod
    def copy_files(source, target):
        files = [
            'resources/icon.png',
            AvatarLanguage.LANGUAGE_PATH,
            'LICENSE-CC-BY-SA-3.0.txt',
            'Readme.md'
        ]

        print('Copying {} static files'.format(len(files)))

        # Keep track of which directories have been created
        dirs = []

        for file in files:
            source_file = os.path.join(source, file)
            target_file = os.path.join(target, file)

            # Ensure directory exists
            target_dir = os.path.dirname(target_file)
            if target_dir and target_dir not in dirs:
                if not os.path.exists(target_dir):
                    print('Creating directory "{}"'.format(target_dir))
                    os.makedirs(target_dir)
                dirs.append(target_dir)

            shutil.copy(source_file, target_file)
