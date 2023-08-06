#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.experiments.base_legacy.tract_seg_legacy import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    FEATURES_FILENAME = "12g90g270g_CSD_BX"

    LR_SCHEDULE = True
    LR_SCHEDULE_MODE = "min"
    LR_SCHEDULE_PATIENCE = 20

    # => 150ep would be enough -> but use 200ep because in some cases LR-reduction might come later because of noise