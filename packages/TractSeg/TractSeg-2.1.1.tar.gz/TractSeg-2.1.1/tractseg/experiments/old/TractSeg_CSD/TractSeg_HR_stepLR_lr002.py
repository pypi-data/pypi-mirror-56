#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.experiments.base_legacy.tract_seg_legacy import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    LEARNING_RATE = 0.002  # 0.001
    LR_SCHEDULE = True

    INFO = "step_size=50, gamma=0.1"

