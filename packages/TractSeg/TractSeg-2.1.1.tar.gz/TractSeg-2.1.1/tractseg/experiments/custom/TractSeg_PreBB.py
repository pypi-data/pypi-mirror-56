#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.experiments.tract_seg import Config as TractSegConfig
from tractseg.libs.system_config import SystemConfig as C


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    RESET_LAST_LAYER = True
    LEARNING_RATE = 0.001
    # LEARNING_RATE = 0.0001
    LOAD_WEIGHTS = True
    WEIGHTS_PATH = os.path.join(C.EXP_PATH, "TractSeg_bb_aPTX_copy/best_weights_ep232.npz")
    # WEIGHTS_PATH = os.path.join(C.EXP_PATH, "TractSeg_REMOVE/best_weights_ep216.npz")

