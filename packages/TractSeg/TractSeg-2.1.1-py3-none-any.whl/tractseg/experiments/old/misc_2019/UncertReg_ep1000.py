#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.dm_reg import Config as DmRegConfig


class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    THRESHOLD = 0.0001
    LABELS_FILENAME = "bundle_uncertainties"
    BEST_EPOCH_SELECTION = "loss"

    NUM_EPOCHS = 1000

