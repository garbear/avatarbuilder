#!/usr/bin/env python3
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

import avatarbuilder

import os
import sys

# TODO: Move this to config file
_AVATAR_REPO = 'https://github.com/kodi-game/OpenGameArt.org.git'

if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))
    builder = avatarbuilder.AvatarBuilder(directory, _AVATAR_REPO)
    success = builder.build()

    sys.exit(0 if success else 1)
