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

from avatarbuilder.AvatarImage import AvatarImage
from avatarbuilder.AvatarLanguage import AvatarLanguage
from avatarbuilder.AvatarRepo import AvatarRepo
from avatarbuilder.AvatarResources import AvatarResources
from avatarbuilder.AvatarXml import AvatarXml

import os


class AvatarBuilder(object):
    _REPO_FOLDER = 'download'
    _BUILD_FOLDER = 'build'
    _RESOURCES_FOLDER = 'resources'
    _AVATARS_FOLDER = 'avatars'

    def __init__(self, directory, repo_url):
        self._directory = directory
        self._repo_url = repo_url

    def build(self):
        # Build repo
        repo_dir = os.path.join(self._directory, AvatarBuilder._REPO_FOLDER)
        repo = self._build_repo(self._repo_url, repo_dir)
        if not repo:
            return False

        # Get avatars
        avatars = self._get_avatars(repo.getpath())

        # Create output folder
        build_dir = os.path.join(self._directory, AvatarBuilder._BUILD_FOLDER)
        resources_dir = os.path.join(build_dir, AvatarBuilder._RESOURCES_FOLDER)
        avatars_dir = os.path.join(resources_dir, AvatarBuilder._AVATARS_FOLDER)
        if not os.path.exists(avatars_dir):
            print('Creating avatars folder "{}"'.format(avatars_dir))
            os.makedirs(avatars_dir)

        print('Saving frames to "{}"'.format(avatars_dir))
        save_avatars = self._generate_frames(avatars, avatars_dir)

        # Copy resources
        AvatarResources.copy_files(repo.getpath(), build_dir)

        language = AvatarLanguage(save_avatars)

        # Save avatars.xml
        avatars_xml_path = os.path.join(resources_dir, AvatarXml.FILE_NAME)
        AvatarXml.save_avatars(save_avatars, language, avatars_xml_path,
                               AvatarBuilder._AVATARS_FOLDER)

        # Generate language file
        language.generate_language(build_dir)

        print('Finished building')

        return True

    @staticmethod
    def _build_repo(repo_url, repo_dir):
        repo = AvatarRepo(repo_dir, repo_url)

        if not repo.isvalid():
            repo.clone()

            if not repo.isvalid():
                return None

        return repo

    @staticmethod
    def _get_avatars(path):
        avatars = []

        for root, dirs, files in os.walk(path):
            for file in files:
                if file == AvatarXml.FILE_NAME:
                    avatars_xml_path = os.path.join(root, file)
                    print('Processing {}'.format(avatars_xml_path))
                    loaded_avatars = AvatarXml.load_avatars(avatars_xml_path)
                    avatars.extend(loaded_avatars)

        return avatars

    @staticmethod
    def _generate_frames(avatars, save_path):
        save_avatars = []

        for avatar in avatars:
            sheet = avatar.sheet()

            # Sanity check
            if not sheet:
                continue

            image = AvatarImage.load_image(sheet.image())
            if image is None:
                print('Error: Avatar "{}" - Failed to load image: "{}"'
                      .format(avatar.name(), sheet.image()))
                continue

            if AvatarImage.generate_frames(image, avatar, save_path):
                save_avatars.append(avatar)

        return save_avatars
