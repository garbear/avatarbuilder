#!/usr/bin/env python
#
# Copyright (C) 2017 Garrett Brown
# See Copyright Notice in GPL-LICENSE.txt
#

import avatarbuilder

import os
import sys


def main(filename):
    builder = avatarbuilder.AvatarBuilder(filename)
    builder.build()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(os.path.abspath(sys.argv[1]))
    else:
        print('Call with image: {} <filename>'.format(sys.argv[0]))
