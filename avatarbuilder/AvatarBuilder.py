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

from avatarbuilder.AvatarRepo import AvatarRepo
from avatarbuilder.AvatarXml import AvatarXml

import os


class AvatarBuilder(object):
    def __init__(self, directory, repo_url):
        self._directory = directory
        self._repo_url = repo_url

    def build(self):
        repo = AvatarRepo(self._directory, self._repo_url)

        if not repo.isvalid():
            print('Cloning repo {}'.format(self._repo_url))
            repo.clone()

            if not repo.isvalid():
                print('Failed to clone repo')
                return False

        avatars = []

        for root, dirs, files in os.walk(repo.getpath()):
            for file in files:
                if file == AvatarXml.FILE_NAME:
                    avatars_xml_path = os.path.join(root, file)
                    print('Processing {}'.format(avatars_xml_path))
                    loaded_avatars = AvatarXml.load_avatars(avatars_xml_path)
                    avatars.extend(loaded_avatars)

        for avatar in avatars:
            print('Found avatar: {}'.format(avatar.name()))

        print('Finished building')

        return True
