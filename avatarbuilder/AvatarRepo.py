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

import git
import os


class AvatarRepo(object):
    def __init__(self, directory, repo):
        # Ensure directory exists
        if not os.path.exists(directory):
            print('Creating directory: "{}"'.format(directory))
            os.makedirs(directory)

        self._directory = self._get_repo_dir(directory, repo)
        self._repo = repo
        self._isvalid = False

    def getpath(self):
        return self._directory

    def clone(self):
        success = False

        print('Cloning repo {}'.format(self._repo))

        try:
            git.Repo.clone_from(self._repo, self._directory)
            success = True
        except git.exc.GitCommandError:
            # Assume already cloned
            success = True
            pass

        if success:
            self._isvalid = True
            return True

        self._isvalid = False
        print('Failed to clone repo')
        return False

    def isvalid(self):
        return self._isvalid

    @staticmethod
    def _get_repo_dir(directory, repo):
        name = os.path.basename(repo)

        # Remove trailing '.git'
        if name[-4:] == '.git':
            name = name[:-4]

        return os.path.join(directory, name)
