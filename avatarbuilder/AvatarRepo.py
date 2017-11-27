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
    _REPO_FOLDER = 'download'

    def __init__(self, directory, repo):
        self._directory = os.path.join(directory, AvatarRepo._REPO_FOLDER)
        self._repo = repo
        self._isvalid = False

    def getpath(self):
        return self._directory

    def clone(self):
        success = False

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

        return False

    def isvalid(self):
        return self._isvalid
