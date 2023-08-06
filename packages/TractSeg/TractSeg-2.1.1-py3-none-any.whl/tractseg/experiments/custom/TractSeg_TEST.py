#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.experiments.tract_seg import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    # DATA_AUGMENTATION = False
    # UNET_NR_FILT = 16
    # BATCH_SIZE = 50
    # NUM_EPOCHS = 1
    # EPOCH_MULTIPLIER = 0.1

    # DAUG_ROTATE = True
    # P_SAMP = 1.

    # NR_OF_GRADIENTS = 18
