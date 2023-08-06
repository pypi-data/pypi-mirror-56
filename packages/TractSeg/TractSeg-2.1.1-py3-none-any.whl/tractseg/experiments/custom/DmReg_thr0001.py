#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.dm_reg import Config as DmRegConfig

class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    THRESHOLD = 0.0001  # use lower value so user has more choice

    NUM_EPOCHS = 350
    BEST_EPOCH_SELECTION = "loss"