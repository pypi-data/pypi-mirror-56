#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.experiments.tract_seg import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    NR_OF_GRADIENTS = 1
    FEATURES_FILENAME = "12g90g270g_FA"

    CV_FOLD = 0
