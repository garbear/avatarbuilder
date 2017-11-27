#
# Copyright (C) 2017 Garrett Brown
# See Copyright Notice in GPL-LICENSE.txt
#

import numpy as np
import cv2


class AvatarBuilder(object):
    def __init__(self, filename):
        self.filename = filename

    def build(self):
        print('Loading {}'.format(self.filename))
